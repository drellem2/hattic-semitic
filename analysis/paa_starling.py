#!/usr/bin/env python3
"""Build data/proto_afroasiatic.tsv from the Militarev-Stolbova database.

The primary Proto-Afroasiatic source (preregistration A4.1, A5) is the
"Afroasiatic etymology" database of the Tower of Babel project, served by
StarLing at starlingdb.org (basename /data/semham/afaset). This script
applies the A4.1 slot rules, as A5 reads them, to that database:

- the gloss of a reconstruction is its "Meaning" field, split into
  components at top-level "," and ";" (A5 rule 1);
- a component is the slot meaning if it is the slot word or a §2
  equivalent, ignoring a leading "to", a trailing "?" and a trailing "(?)";
- the record's reflex fields must cover at least two of the six branches,
  at least one of them not Semitic (A4.1; A5 rule 4);
- ties are broken by: gloss is the slot meaning alone (A5 rule 2), then the
  most branches, then the database's own record order (A5 rule 6);
- homographs are resolved by part of speech as listed in POS_EXCLUDED
  (A5 rule 3).

Each chosen record is re-fetched on its own list page (first=N, where it is
the first record), and the quote "Proto-Afro-Asiatic: <form> Meaning: <gloss>"
is checked to be a substring of that page's text. A form whose quote does not
check is not written.

Usage:
    python3 analysis/paa_starling.py fetch CACHE_DIR
    python3 analysis/paa_starling.py build CACHE_DIR [--viewed YYYY-MM-DD]

`fetch` downloads the full record list (about 134 pages) into CACHE_DIR.
`build` reads it, fetches each chosen record's page into CACHE_DIR/rec if it
is not already there, and writes data/proto_afroasiatic.tsv.
"""

import argparse
import datetime
import html
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_data  # noqa: E402

BASE = "https://starlingdb.org/cgi-bin/response.cgi"
QUERY = "root=config&basename=%2fdata%2fsemham%2fafaset"
WORK = ("Militarev & Stolbova, Afroasiatic etymology "
        "(Tower of Babel, StarLing database afaset)")
LEVEL = "Proto-Afro-Asiatic"
TOTAL_RECORDS = 2671

# Slot words. The first word of each list is the list's own gloss; §2
# equivalents are in SHIFT.
TERMS = {
    1: ["fire"], 2: ["nose"], 3: ["go", "walk"], 4: ["water"], 5: ["mouth"],
    6: ["tongue"], 7: ["blood"], 8: ["bone"], 10: ["root"], 11: ["come"],
    12: ["breast"], 13: ["rain"], 15: ["name"], 16: ["louse", "lice"],
    17: ["wing"], 18: ["flesh", "meat"], 19: ["arm", "hand"], 20: ["fly"],
    21: ["night"], 22: ["ear"], 23: ["neck"], 24: ["far"],
    25: ["do", "make"], 26: ["house"], 27: ["stone", "rock"],
    28: ["bitter"], 29: ["say", "speak"], 30: ["tooth", "teeth"],
    31: ["hair"], 32: ["big"], 33: ["one"], 34: ["who"],
    36: ["hit", "beat"], 37: ["leg", "foot"], 38: ["horn"], 39: ["this"],
    40: ["fish"], 41: ["yesterday"], 42: ["drink"], 43: ["black"],
    44: ["navel"], 45: ["stand"], 46: ["bite"], 47: ["back"], 48: ["wind"],
    49: ["smoke"], 50: ["what"], 51: ["child", "son", "daughter"],
    52: ["egg"], 53: ["give"], 54: ["new"], 55: ["burn"], 57: ["good"],
    58: ["know"], 59: ["knee"], 60: ["sand"], 61: ["laugh"], 62: ["hear"],
    63: ["soil", "earth", "ground"], 64: ["leaf", "leaves"], 65: ["red"],
    66: ["liver"], 67: ["hide"], 68: ["skin", "hide"], 69: ["suck"],
    70: ["carry"], 71: ["ant"], 72: ["heavy"], 73: ["take"], 74: ["old"],
    75: ["eat"], 76: ["thigh"], 77: ["thick"], 78: ["long"], 79: ["blow"],
    80: ["wood", "tree"], 81: ["run"], 82: ["fall"], 83: ["eye"],
    84: ["ash", "ashes"], 85: ["tail"], 86: ["dog"], 87: ["cry", "weep"],
    88: ["tie"], 89: ["see", "look"], 90: ["sweet"], 91: ["rope"],
    92: ["shade", "shadow"], 93: ["bird"], 94: ["salt"], 95: ["small"],
    96: ["wide"], 97: ["star"], 98: ["in"], 99: ["hard"],
    100: ["crush", "grind"],
}
# §2 closed list of further equivalences: a match only through these is
# tagged permitted-shift.
SHIFT = {3: {"walk"}, 29: {"speak"}, 63: {"earth", "ground"}, 80: {"tree"},
         89: {"look"}}

# A5 rule 3: homographs resolved by part of speech. record -> (slots it may
# not fill, reason).
POS_EXCLUDED = {
    2620: ({20}, "'fly' alone; reflexes 'fly (of birds)', 'fly, jump': verb"),
    2030: ({20}, "'fly, soar': verb"),
    469: ({20}, "'to fly, jump': verb"),
    1375: ({20}, "'jump, fly': verb"),
    2454: ({20}, "'fly, go away': verb"),
    1519: ({20}, "'move upwards, fly': verb"),
    764: ({68}, "'hide' alone; reflexes 'cover', 'hide' (Eg dgy, WCh *dag-): verb"),
    2553: ({68}, "'hide' alone; reflexes 'unguarded, unprotected', 'hide': verb"),
    884: ({68}, "'hide, bury': verb"),
    698: ({68}, "'hide, close': verb"),
    2426: ({68}, "'hide, close': verb"),
    32: ({67}, "'hide, skin': noun"),
    751: ({67}, "'skin, hide': noun"),
    1961: ({67}, "'skin, hide': noun"),
    2611: ({67}, "'hide, skin': noun"),
}

# Facts about a slot's gloss that the rules leave open, stated on the row.
SLOT_NOTES = {
    55: "the source's gloss 'burn' does not say whether it is intransitive",
    87: "the source's gloss 'cry' does not say whether it means weep or "
        "shout; the East Chadic reflex is glossed 'a cry'",
}

BRANCH = {
    "Semitic": "Semitic", "Egyptian": "Egyptian", "Berber": "Berber",
    "Western Chadic": "Chadic", "Central Chadic": "Chadic",
    "East Chadic": "Chadic",
    "Beḍauye (Beja)": "Cushitic", "Central Cushitic (Agaw)": "Cushitic",
    "Saho-Afar": "Cushitic", "Low East Cushitic": "Cushitic",
    "High East Cushitic": "Cushitic", "Warazi (Dullay)": "Cushitic",
    "Mogogodo (Yaaku)": "Cushitic", "Dahalo (Sanye)": "Cushitic",
    "South Cushitic": "Cushitic",
    "Omotic": "Omotic",
}
BRANCH_ORDER = ["Semitic", "Egyptian", "Berber", "Chadic", "Cushitic", "Omotic"]
DOUBT_RE = re.compile(r"scarce|doubt|question|uncertain|unclear|\?", re.I)

COLUMNS = validate_data.COLUMNS["proto_afroasiatic.tsv"]


# --- parsing ---------------------------------------------------------------

def _clean(fragment):
    text = html.unescape(re.sub(r"<[^>]*>", " ", fragment))
    return re.sub(r"\s+", " ", text).strip()


def parse_records(page):
    """The records on one list page, each a list of (field, value) pairs."""
    records = []
    for chunk in page.split('<div class="results_record">')[1:]:
        chunk = chunk.split("<!-- results_record_end -->")[0]
        fields = []
        for m in re.finditer(
                r'<span class="fld">(.*?)</span>\s*(.*?)'
                r'(?=<div><span class="fld">|$)', chunk, re.S):
            fields.append((_clean(m.group(1)).rstrip(":"), _clean(m.group(2))))
        records.append(fields)
    return records


def page_text(page):
    """The page's visible text, whitespace-normalised, for quote checks."""
    return _clean(page)


def components(meaning):
    """Split a gloss at "," and ";" outside parentheses."""
    out, cur, depth = [], "", 0
    for ch in meaning:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch in ",;" and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [re.sub(r"\s+", " ", c).strip() for c in out if c.strip()]


def normalise(component):
    """(word, marked_doubtful) for one gloss component (A5 rule 1)."""
    doubtful = "(?)" in component
    c = component.replace("(?)", "").strip()
    c = re.sub(r"^to ", "", c)
    c = re.sub(r"\?$", "", c).strip()
    return c.lower(), doubtful


def branches(record):
    found = {BRANCH[k] for k, _ in record if k in BRANCH}
    return [b for b in BRANCH_ORDER if b in found]


# --- selection -------------------------------------------------------------

def candidates(records, slot):
    """All records whose gloss has the slot meaning as a component.

    Returns (qualifying, failing_branch_rule, near_misses, pos_excluded);
    each item is a dict, and record numbers are 1-based database order.
    """
    words = set(TERMS[slot])
    word_re = re.compile(r"\b(?:" + "|".join(TERMS[slot]) + r")\b", re.I)
    qual, fail, near, pos = [], [], [], []
    for i, rec in enumerate(records):
        n = i + 1
        d = dict(rec)
        meaning = d.get("Meaning", "")
        comps = [normalise(c) for c in components(meaning)]
        hits = [c for c, _ in comps if c in words]
        item = {"n": n, "form": d.get(LEVEL, ""), "meaning": meaning,
                "record": rec}
        if not hits:
            if word_re.search(meaning):
                near.append(item)
            continue
        if n in POS_EXCLUDED and slot in POS_EXCLUDED[n][0]:
            item["reason"] = POS_EXCLUDED[n][1]
            pos.append(item)
            continue
        brs = branches(rec)
        item.update(
            branches=brs,
            alone=all(c in words for c, _ in comps),
            shift=all(h in SHIFT.get(slot, set()) for h in hits),
            gloss_doubtful=any(q for c, q in comps if c in words),
        )
        if len(brs) >= 2 and any(b != "Semitic" for b in brs):
            qual.append(item)
        else:
            fail.append(item)
    qual.sort(key=lambda q: (not q["alone"], -len(q["branches"]), q["n"]))
    return qual, fail, near, pos


# --- output ----------------------------------------------------------------

def record_url(n):
    return f"{BASE}?{QUERY}&first={n}"


def quote_for(item):
    return f"{LEVEL}: {item['form']} Meaning: {item['meaning']}"


def strip_doubt(form):
    return form.replace("(?)", "").strip()


def subgroup_label(record):
    groups = {}
    for k, _ in record:
        if k in BRANCH:
            groups.setdefault(BRANCH[k], []).append(k)
    parts = []
    for b in BRANCH_ORDER:
        if b in groups:
            subs = [s for s in groups[b] if s != b]
            parts.append(f"{b} ({', '.join(subs)})" if subs else b)
    return "; ".join(parts)


def short(item):
    return f"#{item['n']} {item['form']} '{item['meaning']}'"


def notes_for(slot, chosen, qual, fail, near, pos):
    notes = []
    rec = chosen["record"]
    d = dict(rec)
    if "(?)" in chosen["form"]:
        notes.append("the source marks the reconstruction '(?)'")
    if chosen["gloss_doubtful"]:
        notes.append("the source marks the gloss '(?)'")
    doubtful_reflexes = [k for k, v in rec if k in BRANCH and "?" in v]
    if doubtful_reflexes:
        notes.append("reflexes the source marks with '?' (doubtful, or a "
                     "possible loan): " + ", ".join(doubtful_reflexes))
    src_notes = d.get("Notes", "")
    if src_notes and DOUBT_RE.search(src_notes):
        q = src_notes if len(src_notes) <= 300 else src_notes[:300] + " […]"
        notes.append(f"source notes: '{q}'")
    if chosen["n"] in POS_EXCLUDED:
        notes.append("part of speech (A5 rule 3): "
                     + POS_EXCLUDED[chosen["n"]][1])
    others = [q for q in qual if q is not chosen]
    how = ("chosen by A4.1 tie-breakers: "
           + ("gloss is the slot meaning alone" if chosen["alone"]
              else "no record glossed with the slot meaning alone")
           + f", {len(chosen['branches'])} branches, record order")
    notes.append(how)
    if slot in SLOT_NOTES:
        notes.append(SLOT_NOTES[slot])
    if others:
        notes.append(f"{len(others)} other qualifying record(s): "
                     + ", ".join(f"#{q['n']}" for q in others))
    if pos:
        notes.append("excluded by part of speech: "
                     + ", ".join(f"#{p['n']}" for p in pos))
    notes.append("found by gloss search over the full record list")
    return " | ".join(notes)


def empty_notes(slot, fail, near, pos):
    notes = ["no record meets A4.1 for this meaning"]
    if fail:
        notes.append("glossed with the slot meaning but reflexes in fewer "
                     "than two branches or Semitic only: "
                     + "; ".join(f"{short(f)} ({', '.join(f['branches']) or 'none'})"
                                 for f in fail))
    if pos:
        notes.append("excluded by part of speech: "
                     + "; ".join(f"{short(p)} ({p['reason']})" for p in pos))
    if near:
        shown = near[:6]
        more = f" and {len(near) - 6} more" if len(near) > 6 else ""
        notes.append("slot word only inside another meaning: "
                     + "; ".join(short(x) for x in shown) + more)
    notes.append("found by gloss search over the full record list")
    return " | ".join(notes)


def fetch(url, tries=5):
    """A list page from the server; retried, because it intermittently
    answers with an nginx error page instead of records."""
    req = urllib.request.Request(url, headers={"User-Agent": "hattic-semitic research"})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                page = r.read().decode("utf-8")
            if '<div class="results_record">' in page:
                return page
        except OSError:
            pass
        time.sleep(5 * (attempt + 1))
    raise SystemExit(f"no records at {url} after {tries} tries")


def cached(path):
    """A cached page, or None if absent or an error page."""
    if path.exists():
        page = path.read_text(encoding="utf-8")
        if '<div class="results_record">' in page:
            return page
    return None


def load_list(cache):
    records = []
    for first in range(1, TOTAL_RECORDS + 1, 20):
        records += parse_records(
            (cache / f"p{first:04d}.html").read_text(encoding="utf-8"))
    if len(records) != TOTAL_RECORDS:
        raise SystemExit(f"read {len(records)} records, expected {TOTAL_RECORDS}")
    return records


def record_page(cache, n):
    path = cache / "rec" / f"{n}.html"
    page = cached(path)
    if page is None:
        path.parent.mkdir(parents=True, exist_ok=True)
        page = fetch(record_url(n))
        path.write_text(page, encoding="utf-8")
        time.sleep(0.5)
    return page


def check_quote(cache, item):
    """True if the record is first on its first=N page and the quote is there."""
    page = record_page(cache, item["n"])
    recs = parse_records(page)
    return bool(recs) and recs[0] == item["record"] and quote_for(item) in page_text(page)


def build_rows(records, meanings, cache, viewed):
    rows, failures = [], []
    for slot in range(1, 101):
        row = {c: "" for c in COLUMNS}
        row.update(slot=str(slot), meaning=meanings[slot], strand="lexical")
        if slot in validate_data.GRAMMATICAL_SLOTS:
            row.update(strand="morphology",
                       notes="grammatical item: see data/morphology.md")
            rows.append(row)
            continue
        qual, fail, near, pos = candidates(records, slot)
        if not qual:
            row["notes"] = empty_notes(slot, fail, near, pos)
            rows.append(row)
            continue
        c = qual[0]
        if not check_quote(cache, c):
            failures.append(slot)
            row["notes"] = f"quote check failed for {short(c)}; not entered"
            rows.append(row)
            continue
        row.update(
            root=c["form"], form=strip_doubt(c["form"]), level=LEVEL,
            gloss_as_given=c["meaning"],
            match="permitted-shift" if c["shift"] else "exact",
            provenance=f"cited:{WORK}, record {c['n']}; {record_url(c['n'])}",
            branches=subgroup_label(c["record"]),
            non_semitic_branches=str(sum(b != "Semitic" for b in c["branches"])),
            viewed=viewed, quote=quote_for(c),
            notes=notes_for(slot, c, qual, fail, near, pos))
        rows.append(row)
    return rows, failures


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("command", choices=["fetch", "build"])
    ap.add_argument("cache", type=Path)
    ap.add_argument("--viewed", default=datetime.date.today().isoformat())
    args = ap.parse_args(argv[1:])
    root = Path(__file__).resolve().parent.parent
    args.cache.mkdir(parents=True, exist_ok=True)
    if args.command == "fetch":
        for first in range(1, TOTAL_RECORDS + 1, 20):
            path = args.cache / f"p{first:04d}.html"
            if cached(path) is None:
                path.write_text(fetch(f"{BASE}?{QUERY}&first={first}"),
                                encoding="utf-8")
                time.sleep(0.5)
        print(f"{len(load_list(args.cache))} records cached")
        return 0
    records = load_list(args.cache)
    meanings = validate_data.prereg_meanings(root)
    rows, failures = build_rows(records, meanings, args.cache, args.viewed)
    out = root / "data" / "proto_afroasiatic.tsv"
    with out.open("w", encoding="utf-8") as f:
        f.write("\t".join(COLUMNS) + "\n")
        for r in rows:
            f.write("\t".join(r[c] for c in COLUMNS) + "\n")
    filled = sum(1 for r in rows if r["form"])
    print(f"wrote {out.relative_to(root)}: {filled} of 96 lexical slots filled; "
          f"{len(failures)} quote check failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

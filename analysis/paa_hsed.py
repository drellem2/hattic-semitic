#!/usr/bin/env python3
"""Build data/proto_afroasiatic_hsed.tsv from Orel & Stolbova 1995 (HSED).

HSED is the next Proto-Afroasiatic source after the primary one, so A4.1
runs the whole PAA arm on it alone as a sensitivity check that is never
decisive. Amendment A6 states how the A4.1 slot rules, as A5 reads them,
apply to a printed dictionary. This script applies them:

- the gloss of a reconstruction is the gloss printed in its heading, split
  into components at "," and ";" (A6 rule 1, A5 rule 1). A leading "to" and
  a trailing "?" or "(?)" are ignored. Anything else, including a leading
  "be" or "(be)", makes the component a different meaning;
- homographs are resolved by part of speech (A6 rule 3), as listed in
  paa_hsed_data.POS_EXCLUDED;
- the entry's reflex lines must cover at least two of the six branches, at
  least one of them not Semitic (A6 rule 4);
- ties are broken by: gloss is the slot meaning alone, then the most
  branches, then HSED's entry number (A6 rules 2 and 6).

The readings are in paa_hsed_data.py and were taken from the Internet
Archive scan. The OCR misreads most reconstructions, so it was used only to
find entries:

- GLOSS: the heading gloss of every entry the slot search found (A6
  rule 9). Each heading was checked on a contact sheet of heading crops from
  the page images, set beside the OCR reading, and OCR errors were
  corrected. 37 headings whose number the OCR misread were read on the
  image directly.
- LABELS: the family or branch labels of the entry's reflex lines. Where
  the flag is True, they were read on the page image. That covers every
  entry that the tie-breakers compare for a filled slot, every entry that
  could beat the chosen one if a label had been missed, and every entry
  glossed with the slot meaning that fails the branch rule. Where it is
  False, they come from the OCR. Such entries are glossed with the slot
  meaning among other meanings, in a slot that has an entry glossed with it
  alone, so the tie-breakers never reach them. The notes list them
  separately.
- CHOSEN: the reconstruction as printed, transcribed from the page image
  at full resolution.

Usage:
    python3 analysis/paa_hsed.py [--viewed YYYY-MM-DD]
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_data  # noqa: E402
from paa_starling import TERMS, SHIFT  # noqa: E402
from paa_hsed_data import GLOSS, LABELS, CHOSEN, LOCATION, POS_EXCLUDED  # noqa: E402

IDENT = "vladimir-e.-orel-olga-v.-stolbova-hamito-semitic-etymological-dictionary-materia"
SCAN = f"https://archive.org/details/{IDENT}"
WORK = "Orel & Stolbova 1995 (HSED)"
LEVEL = "Hamito-Semitic"
VIEWED = "2026-10-03"

# A6 rule 4: HSED reflex-line labels -> A4.1 branches.
BRANCH = {
    "Sem": "Semitic", "Eg": "Egyptian", "Berb": "Berber",
    "WCh": "Chadic", "CCh": "Chadic", "ECh": "Chadic",
    "Bed": "Cushitic", "Agaw": "Cushitic", "SA": "Cushitic",
    "LEC": "Cushitic", "Wrz": "Cushitic", "HEC": "Cushitic",
    "Dhl": "Cushitic", "Mgg": "Cushitic", "Rift": "Cushitic",
    "Omot": "Omotic",
}
BRANCH_ORDER = ["Semitic", "Egyptian", "Berber", "Chadic", "Cushitic", "Omotic"]
LABEL_ORDER = list(BRANCH)

SLOT_NOTES = {
    55: "the heading gloss 'burn' does not say whether it is intransitive",
    87: "the heading gloss 'cry, weep' fixes the sense as weep",
}

COLUMNS = validate_data.COLUMNS["proto_afroasiatic_hsed.tsv"]


def page_of(leaf, side):
    """Printed page of a column: leaf 19 + k holds pages 2k and 2k + 1."""
    return 2 * (leaf - 19) + (1 if side == "R" else 0)


def url_of(leaf):
    return f"{SCAN}/page/n{leaf}"


def components(gloss):
    return [c.strip() for c in re.split(r"[,;]", gloss) if c.strip()]


def normalise(component):
    c = re.sub(r"^to\s+", "", component.strip())
    c = re.sub(r"\s*\(\?\)$", "", c)
    return re.sub(r"\?$", "", c).strip()


def branches(labels):
    found = {BRANCH[label] for label in labels.split()}
    return [b for b in BRANCH_ORDER if b in found]


def branch_column(labels):
    """'Semitic; Chadic (WCh, CCh)' in the style of proto_afroasiatic.tsv."""
    groups = {}
    for label in sorted(labels.split(), key=LABEL_ORDER.index):
        groups.setdefault(BRANCH[label], []).append(label)
    parts = []
    for b in BRANCH_ORDER:
        if b in groups:
            subs = [s for s in groups[b] if BRANCH[s] != s and s not in
                    ("Sem", "Eg", "Berb", "Omot")]
            parts.append(f"{b} ({', '.join(subs)})" if subs else b)
    return "; ".join(parts)


def candidates(slot):
    """(qualifying, failing, near misses, part-of-speech exclusions)."""
    words = set(TERMS[slot])
    word_re = re.compile(r"\b(?:" + "|".join(TERMS[slot]) + r")\b")
    qual, fail, near, pos = [], [], [], []
    for n, (gloss, tag) in sorted(GLOSS.items()):
        comps = components(gloss)
        hits = [c for c in comps if normalise(c) in words]
        if not hits:
            if word_re.search(gloss):
                near.append({"n": n, "gloss": gloss})
            continue
        key = f"{n}:{slot}"
        if key in POS_EXCLUDED:
            pos.append({"n": n, "gloss": gloss, "reason": POS_EXCLUDED[key]})
            continue
        labels, verified = LABELS[n]
        brs = branches(labels)
        item = {"n": n, "gloss": gloss, "tag": tag, "labels": labels,
                "verified": verified, "branches": brs,
                "alone": all(normalise(c) in words for c in comps),
                "shift": all(normalise(h) in SHIFT.get(slot, set()) for h in hits)}
        if len(brs) >= 2 and any(b != "Semitic" for b in brs):
            qual.append(item)
        else:
            fail.append(item)
    tier = [q for q in qual if q["alone"]] or qual
    tier.sort(key=lambda q: (-len(q["branches"]), q["n"]))
    unread = [t["n"] for t in tier + fail if not t["verified"]]
    if unread:
        raise SystemExit(f"slot {slot}: labels of {unread} not read on the page image")
    rest = [q for q in qual if q not in tier]
    return tier, rest, fail, near, pos


def short(item):
    return f"#{item['n']} '{item['gloss']}'"


def notes_for(slot, chosen, tier, rest, fail, near, pos):
    notes = []
    note = CHOSEN[chosen["n"]][2]
    if note:
        notes.append(note)
    if chosen["tag"]:
        notes.append(f"HSED tags the heading gloss {chosen['tag']}")
    notes.append("chosen by A4.1 tie-breakers: "
                 + ("gloss is the slot meaning alone" if chosen["alone"]
                    else "no qualifying entry glossed with the slot meaning alone")
                 + f", {len(chosen['branches'])} branches, entry order")
    if slot in SLOT_NOTES:
        notes.append(SLOT_NOTES[slot])
    others = [t for t in tier if t is not chosen]
    if others:
        notes.append(f"{len(others)} other qualifying entr"
                     + ("y" if len(others) == 1 else "ies")
                     + " compared by the tie-breakers (branches read on the page image): "
                     + ", ".join(f"#{t['n']} ({len(t['branches'])})" for t in others))
    if rest:
        notes.append("also glossed with the slot meaning among other meanings, "
                     "so not reached by the first tie-breaker: "
                     + ", ".join(f"#{r['n']}" for r in rest))
    if pos:
        notes.append("excluded by part of speech (A6 rule 3): "
                     + "; ".join(f"{short(p)} ({p['reason']})" for p in pos))
    notes.append("found by the Index of Meanings and an OCR heading search "
                 "(A6 rule 9); heading and reflex lines read on the page image")
    return " | ".join(notes)


def empty_notes(slot, fail, near, pos):
    notes = ["no entry meets A4.1 for this meaning"]
    if fail:
        notes.append("glossed with the slot meaning but reflexes in fewer than "
                     "two branches or Semitic only: "
                     + "; ".join(f"{short(f)} ({f['labels'] or 'none'})" for f in fail))
    if pos:
        notes.append("excluded by part of speech (A6 rule 3): "
                     + "; ".join(f"{short(p)} ({p['reason']})" for p in pos))
    if near:
        shown = near[:8]
        more = f" and {len(near) - 8} more" if len(near) > 8 else ""
        notes.append("slot word only inside another meaning: "
                     + "; ".join(short(x) for x in shown) + more)
    if slot in (33, 34, 39, 50, 98):
        notes.append("HSED excludes numerals, pronouns, prepositions and "
                     "particles (p. XXVII; A6 rule 10)")
    notes.append("found by the Index of Meanings and an OCR heading search (A6 rule 9)")
    return " | ".join(notes)


def quote_of(n):
    gloss, tag = GLOSS[n]
    return f"{n} {CHOSEN[n][0]} “{gloss}”" + (f" {tag}" if tag else "")


def build_rows(meanings, viewed=VIEWED):
    rows = []
    for slot in range(1, 101):
        row = {c: "" for c in COLUMNS}
        row.update(slot=str(slot), meaning=meanings[slot], strand="lexical")
        if slot in validate_data.GRAMMATICAL_SLOTS:
            row.update(strand="morphology",
                       notes="grammatical item: see data/morphology.md")
            rows.append(row)
            continue
        tier, rest, fail, near, pos = candidates(slot)
        if not tier:
            row["notes"] = empty_notes(slot, fail, near, pos)
            rows.append(row)
            continue
        c = tier[0]
        if c["n"] not in CHOSEN:
            raise SystemExit(f"slot {slot}: #{c['n']} chosen but not transcribed "
                             "from the page image")
        form, labels, _ = CHOSEN[c["n"]]
        if set(labels.split()) != set(c["labels"].split()):
            raise SystemExit(f"slot {slot}: #{c['n']} labels disagree")
        leaf, side = LOCATION[c["n"]]
        row.update(
            root=form, form=form, level=LEVEL, gloss_as_given=c["gloss"],
            match="permitted-shift" if c["shift"] else "exact",
            provenance=(f"cited:{WORK}, no. {c['n']}, p. {page_of(leaf, side)}; "
                        f"{url_of(leaf)}"),
            branches=branch_column(labels),
            non_semitic_branches=str(sum(b != "Semitic" for b in c["branches"])),
            viewed=viewed, quote=quote_of(c["n"]),
            notes=notes_for(slot, c, tier, rest, fail, near, pos))
        rows.append(row)
    return rows


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--viewed", default=VIEWED)
    args = ap.parse_args(argv[1:])
    root = Path(__file__).resolve().parent.parent
    rows = build_rows(validate_data.prereg_meanings(root), args.viewed)
    out = root / "data" / "proto_afroasiatic_hsed.tsv"
    with out.open("w", encoding="utf-8") as f:
        f.write("\t".join(COLUMNS) + "\n")
        for r in rows:
            f.write("\t".join(r[c] for c in COLUMNS) + "\n")
    filled = sum(1 for r in rows if r["form"])
    print(f"wrote {out.relative_to(root)}: {filled} of 96 lexical slots filled")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

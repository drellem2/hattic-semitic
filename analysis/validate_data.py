#!/usr/bin/env python3
"""Validate the slot lists under data/ and report their counts.

Checks, for data/hattic.tsv, data/proto_semitic.tsv,
data/proto_afroasiatic.tsv, data/proto_afroasiatic_hsed.tsv and every
data/control_*.tsv:

- the header is exactly the expected column list;
- there is one row per Leipzig-Jakarta slot, 1..100 in order, and each
  meaning matches the table in docs/preregistration.md;
- slots 9, 14, 35 and 56 are marked `morphology` and carry no form;
- every non-empty form has a provenance value, which is either
  `uncollated` or `cited:<work, page/entry; where viewed>`; an empty form
  has no provenance;
- controlled-vocabulary columns hold only their allowed values;
- in hattic.tsv, `decision` is `counts` exactly when the form is cited,
  securely glossed and in a lexical slot (preregistration §1.2, A3);
- in proto_afroasiatic.tsv, a filled slot is at the Proto-Afro-Asiatic
  level, has reflexes in at least two branches, one not Semitic (A4.1),
  records the date viewed, and quotes the reconstruction and its gloss;
- in proto_afroasiatic_hsed.tsv (the A4.1 sensitivity list, A6), the same,
  with the source's own level label, Hamito-Semitic; the quote is the entry
  heading, and the cited page lies on the cited scan leaf (A6 rule 7).

Exit status is 0 if every file validates, 1 otherwise. Counts are printed
either way.

Usage: python3 analysis/validate_data.py [repo_root]
"""

import csv
import re
import sys
from pathlib import Path

GRAMMATICAL_SLOTS = {9, 14, 35, 56}

COMMON = ["slot", "meaning", "strand"]
COLUMNS = {
    "hattic.tsv": COMMON + [
        "form", "stem", "segmentation", "gloss_as_given", "gloss_confidence",
        "match", "provenance", "decision", "notes",
    ],
    "proto_semitic.tsv": COMMON + [
        "root", "form", "level", "gloss_as_given", "match", "provenance",
        "notes",
    ],
    "proto_afroasiatic.tsv": COMMON + [
        "root", "form", "level", "gloss_as_given", "match", "provenance",
        "branches", "non_semitic_branches", "viewed", "quote", "notes",
    ],
    "control": COMMON + [
        "form", "gloss_as_given", "match", "provenance", "notes",
    ],
}

COLUMNS["proto_afroasiatic_hsed.tsv"] = COLUMNS["proto_afroasiatic.tsv"]

ALLOWED = {
    "strand": {"lexical", "morphology"},
    "gloss_confidence": {"", "secure", "doubtful"},
    "match": {"", "exact", "permitted-shift"},
    "decision": {"", "counts", "exploratory"},
}

# cited:<work>, <page or entry>; <where viewed>
CITED_RE = re.compile(r"^cited:[^;]+,[^;]+;\s*\S+")


def prereg_meanings(root):
    """Slot -> meaning, read from the §1 table of the preregistration."""
    text = (root / "docs" / "preregistration.md").read_text(encoding="utf-8")
    meanings = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        for i in range(0, 8, 2):
            if cells[i].isdigit():
                meanings[int(cells[i])] = cells[i + 1]
    return meanings


def provenance_ok(value):
    return value == "uncollated" or bool(CITED_RE.match(value))


def validate_file(path, columns, meanings):
    """Return (errors, rows) for one TSV file."""
    errors = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        if reader.fieldnames != columns:
            return [f"{path.name}: header {reader.fieldnames} != {columns}"], []
        rows = list(reader)

    if [r["slot"] for r in rows] != [str(n) for n in range(1, 101)]:
        errors.append(f"{path.name}: slots must be 1..100 in order")

    for r in rows:
        where = f"{path.name} slot {r['slot']}"
        if None in r or any(v is None for v in r.values()):
            errors.append(f"{where}: wrong number of fields")
            continue
        slot = int(r["slot"]) if r["slot"].isdigit() else None
        if slot in meanings and r["meaning"] != meanings[slot]:
            errors.append(
                f"{where}: meaning {r['meaning']!r} != preregistered "
                f"{meanings[slot]!r}")
        for col, allowed in ALLOWED.items():
            if col in r and r[col] not in allowed:
                errors.append(f"{where}: {col}={r[col]!r} not in {sorted(allowed)}")
        expected_strand = "morphology" if slot in GRAMMATICAL_SLOTS else "lexical"
        if r["strand"] != expected_strand:
            errors.append(f"{where}: strand must be {expected_strand}")

        form, prov = r["form"], r["provenance"]
        if form:
            if not provenance_ok(prov):
                errors.append(f"{where}: form {form!r} has bad provenance {prov!r}")
            if r["strand"] == "morphology":
                errors.append(f"{where}: grammatical slot must not carry a form")
            if not r["match"]:
                errors.append(f"{where}: form without match tag")
        else:
            for col in ("provenance", "match", "gloss_confidence", "decision",
                        "stem", "segmentation", "gloss_as_given", "root",
                        "level", "branches", "non_semitic_branches", "viewed",
                        "quote"):
                if r.get(col):
                    errors.append(f"{where}: {col} set but form is empty")

        if "quote" in r and form:
            errors += paa_errors(where, r, PAA_LEVEL[path.name])

        if "decision" in r and form:
            qualifies = (prov.startswith("cited:")
                         and r["gloss_confidence"] == "secure"
                         and r["strand"] == "lexical")
            want = "counts" if qualifies else "exploratory"
            if r["decision"] != want:
                errors.append(f"{where}: decision must be {want!r}")
            if not r["gloss_confidence"]:
                errors.append(f"{where}: form without gloss_confidence")
    return errors, rows


PAA_BRANCHES = ("Semitic", "Egyptian", "Berber", "Chadic", "Cushitic", "Omotic")
# Each source's own label for the Proto-Afroasiatic level (A5 rule 5, A6 rule 5).
PAA_LEVEL = {"proto_afroasiatic.tsv": "Proto-Afro-Asiatic",
             "proto_afroasiatic_hsed.tsv": "Hamito-Semitic"}
# A6 rule 7: cited:<work>, no. N, p. P; <scan>/page/n<leaf>
HSED_PROV_RE = re.compile(r"^cited:[^;]+, no\. (\d+), p\. (\d+); \S+/page/n(\d+)$")


def paa_errors(where, r, level):
    """A4.1 / A5 / A6 checks on one filled Proto-Afroasiatic row."""
    errors = []
    if r["level"] != level:
        errors.append(f"{where}: level must be {level!r} (A4.1)")
    named = [b.split(" (")[0] for b in r["branches"].split("; ") if b]
    if any(b not in PAA_BRANCHES for b in named) or len(set(named)) != len(named):
        errors.append(f"{where}: branches {r['branches']!r} not a list of the six branches")
    nonsem = sum(b != "Semitic" for b in named)
    if len(named) < 2 or nonsem < 1:
        errors.append(f"{where}: needs at least two branches, one not Semitic (A4.1)")
    if r["non_semitic_branches"] != str(nonsem):
        errors.append(f"{where}: non_semitic_branches must be {nonsem}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["viewed"]):
        errors.append(f"{where}: viewed must be a YYYY-MM-DD date (A4.1)")
    if level == "Hamito-Semitic":
        m = HSED_PROV_RE.match(r["provenance"])
        if not m:
            errors.append(f"{where}: provenance must cite entry, page and scan leaf (A6 rule 7)")
        else:
            entry, page, leaf = map(int, m.groups())
            if leaf != 19 + page // 2:
                errors.append(f"{where}: p. {page} is not on scan leaf n{leaf} (A6 rule 7)")
            if not r["quote"].startswith(f"{entry} {r['root']} “{r['gloss_as_given']}”"):
                errors.append(f"{where}: quote must be the heading of entry {entry}: "
                              "number, reconstruction and gloss")
    elif (f"Meaning: {r['gloss_as_given']}" not in r["quote"]
          or r["root"] not in r["quote"]):
        errors.append(f"{where}: quote must contain the reconstruction and its gloss")
    return errors


def summarise(name, rows):
    filled = [r for r in rows if r["form"]]
    cited = [r for r in filled if r["provenance"].startswith("cited:")]
    line = (f"{name}: {len(filled)} of 96 lexical slots filled; "
            f"{len(cited)} cited, {len(filled) - len(cited)} uncollated")
    if filled:
        line += f" ({100 * (len(filled) - len(cited)) / len(filled):.0f}% uncollated)"
    if rows and "decision" in rows[0]:
        counts = sum(r["decision"] == "counts" for r in rows)
        doubtful = sum(r["gloss_confidence"] == "doubtful" for r in filled)
        line += (f"; {counts} count toward the decision (cited + secure), "
                 f"{doubtful} doubtful gloss")
    if rows and "level" in rows[0] and "quote" not in rows[0]:
        lower = sum(1 for r in filled if r["level"] not in
                    ("Common Semitic", "Proto-Semitic"))
        if lower:
            line += f"; {lower} at a level below Proto-Semitic"
    return line


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    data = root / "data"
    meanings = prereg_meanings(root)
    if len(meanings) != 100:
        print(f"could not read 100 meanings from the preregistration ({len(meanings)})")
        return 1

    targets = [("hattic.tsv", COLUMNS["hattic.tsv"]),
               ("proto_semitic.tsv", COLUMNS["proto_semitic.tsv"]),
               ("proto_afroasiatic.tsv", COLUMNS["proto_afroasiatic.tsv"]),
               ("proto_afroasiatic_hsed.tsv", COLUMNS["proto_afroasiatic_hsed.tsv"])]
    targets += [(p.name, COLUMNS["control"])
                for p in sorted(data.glob("control_*.tsv"))]

    all_errors = []
    for name, columns in targets:
        path = data / name
        if not path.exists():
            all_errors.append(f"{name}: missing")
            continue
        errors, rows = validate_file(path, columns, meanings)
        all_errors += errors
        if rows:
            print(summarise(name, rows))
    for e in all_errors:
        print("ERROR", e)
    print("OK" if not all_errors else f"{len(all_errors)} error(s)")
    return 0 if not all_errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

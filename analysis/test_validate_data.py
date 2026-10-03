#!/usr/bin/env python3
"""Tests for validate_data.py. Run: python3 -m unittest analysis/test_validate_data.py"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_data as v  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CITE = "cited:Some Work 1999, p. 12; https://example.org/scan"


def blank_rows(columns, meanings):
    rows = []
    for n in range(1, 101):
        r = {c: "" for c in columns}
        r.update(slot=str(n), meaning=meanings[n],
                 strand="morphology" if n in v.GRAMMATICAL_SLOTS else "lexical")
        rows.append(r)
    return rows


def write(path, columns, rows):
    with path.open("w", encoding="utf-8") as f:
        f.write("\t".join(columns) + "\n")
        for r in rows:
            f.write("\t".join(r[c] for c in columns) + "\n")


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "docs").mkdir()
        (self.root / "data").mkdir()
        shutil.copy(REPO / "docs" / "preregistration.md", self.root / "docs")
        self.meanings = v.prereg_meanings(self.root)
        self.cols = v.COLUMNS["hattic.tsv"]
        self.path = self.root / "data" / "hattic.tsv"

    def tearDown(self):
        shutil.rmtree(self.root)

    def check(self, rows):
        write(self.path, self.cols, rows)
        errors, _ = v.validate_file(self.path, self.cols, self.meanings)
        return errors

    def test_reads_100_meanings(self):
        self.assertEqual(len(self.meanings), 100)
        self.assertEqual(self.meanings[1], "fire")
        self.assertEqual(self.meanings[100], "to crush/grind")

    def test_empty_list_is_valid(self):
        self.assertEqual(self.check(blank_rows(self.cols, self.meanings)), [])

    def test_cited_secure_form_counts(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[3].update(form="x", gloss_as_given="Wasser", gloss_confidence="secure",
                       match="exact", provenance=CITE, decision="counts")
        self.assertEqual(self.check(rows), [])

    def test_form_without_provenance_rejected(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[3].update(form="x", gloss_confidence="secure", match="exact",
                       decision="exploratory")
        self.assertTrue(any("bad provenance" in e for e in self.check(rows)))

    def test_cited_without_page_and_location_rejected(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[3].update(form="x", gloss_confidence="secure", match="exact",
                       provenance="cited:Soysal 2004", decision="counts")
        self.assertTrue(any("bad provenance" in e for e in self.check(rows)))

    def test_uncollated_cannot_count(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[3].update(form="x", gloss_confidence="secure", match="exact",
                       provenance="uncollated", decision="counts")
        self.assertTrue(any("decision must be 'exploratory'" in e
                            for e in self.check(rows)))

    def test_doubtful_cannot_count(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[3].update(form="x", gloss_confidence="doubtful", match="exact",
                       provenance=CITE, decision="counts")
        self.assertTrue(any("decision must be 'exploratory'" in e
                            for e in self.check(rows)))

    def test_grammatical_slot_must_be_empty(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[8].update(form="x", gloss_confidence="secure", match="exact",
                       provenance=CITE, decision="exploratory")
        self.assertTrue(any("grammatical slot" in e for e in self.check(rows)))

    def test_provenance_without_form_rejected(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[3].update(provenance=CITE)
        self.assertTrue(any("form is empty" in e for e in self.check(rows)))

    def test_wrong_meaning_rejected(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[0]["meaning"] = "flame"
        self.assertTrue(any("preregistered" in e for e in self.check(rows)))

    def test_missing_slot_rejected(self):
        rows = blank_rows(self.cols, self.meanings)
        del rows[50]
        self.assertTrue(any("1..100" in e for e in self.check(rows)))


PAA_ROW = dict(
    root="*dam-", form="*dam-", level="Proto-Afro-Asiatic", gloss_as_given="blood",
    match="exact", provenance=CITE,
    branches="Semitic; Egyptian; Chadic (Western Chadic)",
    non_semitic_branches="2", viewed="2026-10-03",
    quote="Proto-Afro-Asiatic: *dam- Meaning: blood")


class ValidateAfroasiaticTest(ValidateTest):
    def setUp(self):
        super().setUp()
        self.cols = v.COLUMNS["proto_afroasiatic.tsv"]
        self.path = self.root / "data" / "proto_afroasiatic.tsv"

    def row(self, **changes):
        rows = blank_rows(self.cols, self.meanings)
        rows[6].update(PAA_ROW)
        rows[6].update(changes)
        return rows

    # The Hattic-specific tests do not apply to this file.
    test_cited_secure_form_counts = None
    test_form_without_provenance_rejected = None
    test_cited_without_page_and_location_rejected = None
    test_uncollated_cannot_count = None
    test_doubtful_cannot_count = None
    test_grammatical_slot_must_be_empty = None

    def test_valid_row(self):
        self.assertEqual(self.check(self.row()), [])

    def test_semitic_only_rejected(self):
        errors = self.check(self.row(branches="Semitic", non_semitic_branches="0"))
        self.assertTrue(any("two branches" in e for e in errors))

    def test_one_branch_rejected(self):
        errors = self.check(self.row(branches="Egyptian", non_semitic_branches="1"))
        self.assertTrue(any("two branches" in e for e in errors))

    def test_non_semitic_count_must_agree(self):
        errors = self.check(self.row(non_semitic_branches="3"))
        self.assertTrue(any("non_semitic_branches must be 2" in e for e in errors))

    def test_unknown_branch_rejected(self):
        errors = self.check(self.row(branches="Semitic; Sumerian", non_semitic_branches="1"))
        self.assertTrue(any("six branches" in e for e in errors))

    def test_lower_level_rejected(self):
        errors = self.check(self.row(level="Proto-Chadic"))
        self.assertTrue(any("Proto-Afro-Asiatic" in e for e in errors))

    def test_view_date_required(self):
        errors = self.check(self.row(viewed=""))
        self.assertTrue(any("viewed" in e for e in errors))

    def test_quote_must_carry_gloss(self):
        errors = self.check(self.row(quote="Proto-Afro-Asiatic: *dam- Meaning: red"))
        self.assertTrue(any("quote" in e for e in errors))

    def test_quote_without_form_rejected(self):
        rows = blank_rows(self.cols, self.meanings)
        rows[6].update(quote="Proto-Afro-Asiatic: *dam- Meaning: blood")
        self.assertTrue(any("form is empty" in e for e in self.check(rows)))


if __name__ == "__main__":
    unittest.main()

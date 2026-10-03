#!/usr/bin/env python3
"""Tests for paa_hsed.py. Run: python3 -m unittest analysis/test_paa_hsed.py"""

import csv
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paa_hsed as p  # noqa: E402
import validate_data  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def patched(gloss, labels, pos=None):
    """Run candidates() over a small invented dictionary."""
    return mock.patch.multiple(p, GLOSS=gloss, LABELS=labels,
                               POS_EXCLUDED=pos or {})


class RulesTest(unittest.TestCase):
    def test_page_and_leaf(self):
        # Leaf 19 + k holds pages 2k (left) and 2k + 1 (right), A6 rule 7.
        self.assertEqual(p.page_of(38, "L"), 38)
        self.assertEqual(p.page_of(38, "R"), 39)
        self.assertEqual(p.page_of(92, "R"), 147)

    def test_branch_mapping(self):
        self.assertEqual(p.branches("Sem Eg WCh CCh LEC Rift Omot"),
                         ["Semitic", "Egyptian", "Chadic", "Cushitic", "Omotic"])
        self.assertEqual(p.branch_column("Omot WCh Sem CCh Bed"),
                         "Semitic; Chadic (WCh, CCh); Cushitic (Bed); Omotic")

    def test_language_label_is_not_a_branch_label(self):
        # 'Ome' (Ometo) is not one of the A6 rule 4 labels.
        with self.assertRaises(KeyError):
            p.branches("Eg Ome")

    def test_be_x_is_not_x(self):
        # A6 rule 1: "be big" does not fill slot 32 big.
        with patched({1: ("be big", "")}, {1: ("Sem Eg", True)}):
            tier, rest, fail, near, pos = p.candidates(32)
        self.assertEqual(tier, [])
        self.assertEqual([x["n"] for x in near], [1])

    def test_trailing_question_mark_ignored(self):
        with patched({1: ("fall?", "")}, {1: ("Sem Eg", True)}):
            tier = p.candidates(82)[0]
        self.assertEqual([t["n"] for t in tier], [1])

    def test_alone_beats_more_branches(self):
        gloss = {1: ("stone, mountain", ""), 2: ("stone", "")}
        labels = {1: ("Sem Eg Berb WCh", True), 2: ("Sem Eg", True)}
        with patched(gloss, labels):
            tier, rest = p.candidates(27)[:2]
        self.assertEqual([t["n"] for t in tier], [2])
        self.assertEqual([r["n"] for r in rest], [1])

    def test_branches_then_entry_order(self):
        gloss = {5: ("stone", ""), 7: ("stone", ""), 9: ("stone", "")}
        labels = {5: ("Sem Eg", True), 7: ("Eg WCh LEC", True),
                  9: ("Berb ECh Omot", True)}
        with patched(gloss, labels):
            tier = p.candidates(27)[0]
        self.assertEqual([t["n"] for t in tier], [7, 9, 5])

    def test_subfamilies_of_one_branch_count_once(self):
        with patched({1: ("water", "")}, {1: ("WCh CCh ECh", True)}):
            tier, rest, fail = p.candidates(4)[:3]
        self.assertEqual(tier, [])
        self.assertEqual([f["n"] for f in fail], [1])

    def test_semitic_plus_one_qualifies(self):
        with patched({1: ("water", "")}, {1: ("Sem Eg", True)}):
            self.assertEqual(len(p.candidates(4)[0]), 1)

    def test_part_of_speech_exclusion(self):
        gloss = {1: ("fly", "(v.)"), 2: ("fly", "(n.)")}
        labels = {1: ("Sem Eg", True), 2: ("Sem Eg", True)}
        with patched(gloss, labels, {"1:20": "verb"}):
            tier, rest, fail, near, pos = p.candidates(20)
        self.assertEqual([t["n"] for t in tier], [2])
        self.assertEqual([x["n"] for x in pos], [1])

    def test_permitted_shift(self):
        with patched({1: ("tree", "")}, {1: ("Sem Eg", True)}):
            self.assertTrue(p.candidates(80)[0][0]["shift"])
        with patched({1: ("wood", "")}, {1: ("Sem Eg", True)}):
            self.assertFalse(p.candidates(80)[0][0]["shift"])

    def test_unread_labels_refused(self):
        # Every entry the tie-breakers compare must have labels read on the image.
        with patched({1: ("stone", "")}, {1: ("Sem Eg", False)}):
            with self.assertRaises(SystemExit):
                p.candidates(27)


class CommittedFileTest(unittest.TestCase):
    """The committed list is what the builder writes, and it validates."""

    def test_rebuild_matches_committed_file(self):
        rows = p.build_rows(validate_data.prereg_meanings(REPO))
        with (REPO / "data" / "proto_afroasiatic_hsed.tsv").open(encoding="utf-8") as f:
            committed = list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
        self.assertEqual([dict(r) for r in committed], rows)

    def test_every_chosen_entry_was_transcribed(self):
        rows = p.build_rows(validate_data.prereg_meanings(REPO))
        chosen = {int(r["quote"].split()[0]) for r in rows if r["form"]}
        self.assertEqual(chosen, set(p.CHOSEN))
        self.assertTrue(chosen <= set(p.LOCATION))

    def test_committed_file_validates(self):
        path = REPO / "data" / "proto_afroasiatic_hsed.tsv"
        errors, _ = validate_data.validate_file(
            path, validate_data.COLUMNS["proto_afroasiatic_hsed.tsv"],
            validate_data.prereg_meanings(REPO))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Tests for paa_starling.py. Run: python3 -m unittest analysis/test_paa_starling.py"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paa_starling as p  # noqa: E402


def rec(form, meaning, *branches, notes=None):
    r = [("Proto-Afro-Asiatic", form), ("Meaning", meaning)]
    r += [(b, "*x- 'y'") for b in branches]
    if notes:
        r.append(("Notes", notes))
    return r


def page(*records):
    """A list page in the server's markup."""
    out = ['<html><body><div class="basename">/data/semham/afaset</div>']
    for r in records:
        out.append('<div class="results_record">')
        for k, v in r:
            out.append(f'<div><span class="fld">{k}:</span> '
                       f'<span class="unicode">{v}</span></div>')
        out.append("<!-- results_record_end --></div>")
    out.append("</body></html>")
    return "".join(out)


class GlossTest(unittest.TestCase):
    def test_components_split_outside_parentheses_only(self):
        self.assertEqual(p.components("k. of insect (bee, fly; locust)"),
                         ["k. of insect (bee, fly; locust)"])
        self.assertEqual(p.components("bug, beetle; fly"), ["bug", "beetle", "fly"])

    def test_normalise(self):
        self.assertEqual(p.normalise("to burn"), ("burn", False))
        self.assertEqual(p.normalise("what?"), ("what", False))
        self.assertEqual(p.normalise("hide (?)"), ("hide", True))
        self.assertEqual(p.normalise("go away"), ("go away", False))

    def test_branches_group_subgroups(self):
        r = rec("*a-", "fire", "Western Chadic", "East Chadic", "Saho-Afar", "Omotic")
        self.assertEqual(p.branches(r), ["Chadic", "Cushitic", "Omotic"])
        self.assertEqual(p.subgroup_label(r),
                         "Chadic (Western Chadic, East Chadic); Cushitic (Saho-Afar); Omotic")


class SelectTest(unittest.TestCase):
    def test_attestation_rule(self):
        records = [rec("*a-", "fire", "Semitic"),
                   rec("*b-", "fire", "Semitic", "Semitic"),
                   rec("*c-", "fire", "Egyptian")]
        qual, fail, _, _ = p.candidates(records, 1)
        self.assertEqual(qual, [])
        self.assertEqual([f["n"] for f in fail], [1, 2, 3])

    def test_semitic_plus_one_qualifies(self):
        qual, _, _, _ = p.candidates([rec("*a-", "fire", "Semitic", "Omotic")], 1)
        self.assertEqual([q["n"] for q in qual], [1])

    def test_tie_breakers(self):
        records = [
            rec("*a-", "fire, coal", "Semitic", "Egyptian", "Berber", "Omotic"),
            rec("*b-", "fire", "Semitic", "Egyptian"),
            rec("*c-", "fire", "Semitic", "Egyptian", "Berber"),
            rec("*d-", "fire", "Semitic", "Egyptian", "Berber"),
        ]
        qual, _, _, _ = p.candidates(records, 1)
        # alone first, then most branches, then record order
        self.assertEqual([q["n"] for q in qual], [3, 4, 2, 1])

    def test_near_miss_does_not_fill(self):
        qual, _, near, _ = p.candidates([rec("*a-", "go away", "Semitic", "Egyptian"),
                                         rec("*b-", "be far", "Semitic", "Egyptian")], 3)
        self.assertEqual(qual, [])
        self.assertEqual([x["n"] for x in near], [1])

    def test_permitted_shift_tag(self):
        qual, _, _, _ = p.candidates([rec("*a-", "earth", "Semitic", "Egyptian"),
                                      rec("*b-", "soil, earth", "Semitic", "Egyptian")], 63)
        self.assertEqual([(q["n"], q["shift"]) for q in qual], [(1, True), (2, False)])

    def test_part_of_speech_exclusion(self):
        records = [rec("*a-", "x", "Semitic", "Egyptian")] * 2619
        records.append(rec("*ʒaw-/*ʒay-", "fly", "East Chadic", "South Cushitic"))
        qual, _, _, pos = p.candidates(records, 20)
        self.assertEqual(qual, [])
        self.assertEqual([x["n"] for x in pos], [2620])


class QuoteTest(unittest.TestCase):
    def setUp(self):
        self.cache = Path(tempfile.mkdtemp())
        (self.cache / "rec").mkdir()

    def tearDown(self):
        shutil.rmtree(self.cache)

    def item(self, n, r):
        d = dict(r)
        return {"n": n, "form": d["Proto-Afro-Asiatic"], "meaning": d["Meaning"], "record": r}

    def test_quote_found_when_record_is_first(self):
        r = rec("*dam-", "blood", "Semitic", "Egyptian")
        (self.cache / "rec" / "786.html").write_text(
            page(r, rec("*x-", "other", "Semitic", "Omotic")), encoding="utf-8")
        self.assertTrue(p.check_quote(self.cache, self.item(786, r)))

    def test_quote_rejected_when_another_record_is_first(self):
        r = rec("*dam-", "blood", "Semitic", "Egyptian")
        (self.cache / "rec" / "786.html").write_text(
            page(rec("*x-", "other", "Semitic", "Omotic"), r), encoding="utf-8")
        self.assertFalse(p.check_quote(self.cache, self.item(786, r)))

    def test_quote_rejected_when_gloss_differs(self):
        r = rec("*dam-", "blood", "Semitic", "Egyptian")
        (self.cache / "rec" / "786.html").write_text(
            page(rec("*dam-", "blood, red", "Semitic", "Egyptian")), encoding="utf-8")
        self.assertFalse(p.check_quote(self.cache, self.item(786, r)))

    def test_error_page_is_not_a_cached_page(self):
        path = self.cache / "rec" / "1.html"
        path.write_text("<html>An error occurred.</html>", encoding="utf-8")
        self.assertIsNone(p.cached(path))


if __name__ == "__main__":
    unittest.main()

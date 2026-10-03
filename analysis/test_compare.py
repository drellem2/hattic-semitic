#!/usr/bin/env python3
"""Tests for compare.py. Run: python3 -m unittest analysis/test_compare.py"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare as c  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def phs(segs):
    return [s.ph for s in segs]


def item(slot, stem, root):
    return {"slot": slot, "h_stem": stem, "ref_root": root,
            "h": c.hattic_consonants(stem), "ref": c.ps_consonants(root)}


class ConsonantsTest(unittest.TestCase):
    def test_hattic_doubled_writing_is_single(self):
        self.assertEqual(phs(c.hattic_consonants("tittaḫ")), ["t", "t", "ḫ"])
        self.assertEqual(phs(c.hattic_consonants("pipiz(z)il")),
                         ["p", "p", "z", "l"])

    def test_hattic_glides_and_wa_series(self):
        self.assertEqual([(s.ph, s.cls) for s in c.hattic_consonants("i̯a")],
                         [("y", "W")])
        self.assertEqual([s.cls for s in c.hattic_consonants("vae")], ["P"])

    def test_hattic_voicing_ignored(self):
        self.assertEqual(phs(c.hattic_consonants("bu")), ["p"])

    def test_hattic_first_alternative(self):
        self.assertEqual(phs(c.hattic_consonants("anna/ana")), ["n"])

    def test_ps_root(self):
        self.assertEqual(phs(c.ps_consonants("ḏwḏ1")), ["ḏ", "w", "ḏ"])
        segs = c.ps_consonants("ʾrṣ́")
        self.assertEqual(phs(segs), ["ʾ", "r", "ṣ́"])
        self.assertTrue(segs[0].skippable)
        self.assertEqual(segs[2].cls, "S")

    def test_pu_first_form_and_vowels(self):
        self.assertEqual(phs(c.pu_consonants("ȣ̈kɜ (jȣ̈kɜ), ȣ̈γɜ (jȣ̈γɜ)")),
                         ["k"])
        self.assertEqual(phs(c.pu_consonants("*po/uxlɨ")), ["p", "x", "l"])
        self.assertEqual(phs(c.pu_consonants("attɜ-")), ["t", "t"])
        self.assertEqual(phs(c.pu_consonants("attɜ-",
                                             collapse_geminates=True)), ["t"])

    def test_every_compared_symbol_is_classed(self):
        hattic = c.read_tsv(REPO / "data" / "hattic.tsv")
        ps = c.read_tsv(REPO / "data" / "proto_semitic.tsv")
        pu = c.read_tsv(REPO / "data" / "control_proto_uralic.tsv")
        for r in hattic.values():
            if r["stem"]:
                for s in c.hattic_consonants(r["stem"]):
                    self.assertIsNotNone(s.cls, (r["slot"], s.ph))
        for r in ps.values():
            if r["root"]:
                for s in c.ps_consonants(r["root"]):
                    self.assertIsNotNone(s.cls, (r["slot"], s.ph))
        for r in pu.values():
            if r["form"]:
                for s in c.pu_consonants(r["form"]):
                    self.assertIsNotNone(s.cls, (r["slot"], s.ph))


class AlignTest(unittest.TestCase):
    def test_two_matches_is_candidate(self):
        a = c.align(c.hattic_consonants("kanab"), c.ps_consonants("knp"))
        self.assertTrue(a["candidate"])
        self.assertEqual(a["matches"], 3)

    def test_t_s_cross_class(self):
        a = c.align(c.hattic_consonants("zan"), c.ps_consonants("tn"))
        self.assertTrue(a["candidate"])

    def test_mismatch_in_first_two_blocks(self):
        a = c.align(c.hattic_consonants("kamat"), c.ps_consonants("knt"))
        self.assertFalse(a["candidate"])  # m ~ n in position 2

    def test_guttural_aligned_with_nothing(self):
        a = c.align(c.hattic_consonants("ramat"), c.ps_consonants("ʾrmt"))
        self.assertTrue(a["candidate"])
        self.assertEqual(a["skipped"], "ʾ")
        a = c.align(c.hattic_consonants("ramat"), c.ps_consonants("ʾʿrm"))
        self.assertFalse(a["candidate"])  # only one guttural may be skipped

    def test_hattic_h_matches_guttural(self):
        a = c.align(c.hattic_consonants("ḫal"), c.ps_consonants("ḥl"))
        self.assertTrue(a["candidate"])
        self.assertIsNone(a["skipped"])

    def test_monoconsonantal_never_candidate(self):
        a = c.align(c.hattic_consonants("nu"), c.ps_consonants("n"))
        self.assertFalse(a["candidate"])


class RegularityTest(unittest.TestCase):
    def test_max_independent(self):
        self.assertEqual(c.max_independent({("a", "x"), ("a", "y"),
                                            ("b", "x")}), 2)
        self.assertEqual(c.max_independent({("a", "x"), ("b", "y"),
                                            ("c", "z")}), 3)

    def test_positive_control_regular_sets_and_shuffle(self):
        # A Hattic list that reflects Proto-Semitic regularly (*k > k,
        # *n > n, *t > z, *b > p, *r > l): the procedure must find it.
        roots = ["knt", "kbr", "krn", "ntk", "nbr", "nrt", "tkb", "tnr",
                 "tbk", "bkn", "btr", "brk", "rkt", "rnb", "rtn"]
        sub = {"k": "k", "n": "n", "t": "z", "b": "p", "r": "l"}
        items = [item(i, "a".join(sub[x] for x in r) + "a", r)
                 for i, r in enumerate(roots, 1)]
        res = c.run(items)
        self.assertEqual(res["candidates"], len(roots))
        self.assertGreaterEqual(res["R"], 5)
        ctl = c.shuffle_control(items, res["R"])
        self.assertLessEqual(ctl["p"], 0.01)

    def test_unconditioned_competing_reflex_does_not_count(self):
        # *t > t and *t > z, each in three independent pairs, initial
        # position, with no conditioning stated: only one may count.
        roots = ["tnk", "tbk", "trk", "tnb", "tbn", "trn"]
        stems = ["tanak", "tapak", "talak", "zanap", "zapan", "zalan"]
        items = [item(i, s, r) for i, (s, r) in enumerate(zip(stems, roots))]
        res = c.run(items)
        regular = {(x["ref"], x["hattic"], x["position"])
                   for x in res["correspondences"] if x["regular"]}
        self.assertIn(("t", "t", "initial"), regular)
        self.assertIn(("t", "z", "initial"), regular)
        competitors = [x for x in res["correspondences"]
                       if x["unconditioned_competitor"]]
        self.assertEqual(len(competitors), 1)

    def test_derangement_has_no_fixed_point(self):
        import random
        rng = random.Random(1)
        for _ in range(50):
            d = c.derangement(rng, 5)
            self.assertTrue(all(i != j for i, j in enumerate(d)))


class OutcomeTest(unittest.TestCase):
    def test_categories(self):
        self.assertEqual(c.outcome(29, True, True, True)[0],
                         "the data cannot decide")
        self.assertEqual(c.outcome(30, False, True, True)[0], "no support")
        self.assertEqual(c.outcome(30, True, False, False)[0],
                         "the data cannot decide")
        self.assertEqual(c.outcome(30, True, True, False)[0],
                         "the data cannot decide")
        self.assertEqual(c.outcome(30, True, True, True)[0], "support")

    def test_lexical_strand(self):
        self.assertTrue(c.lexical_strand(40, 6, 0.01, 0.15, 0.02, 30)[0])
        self.assertFalse(c.lexical_strand(40, 6, 0.01, 0.15, 0.10, 30)[0])
        # n_PU < 20: control B uninformative, p must be <= 0.01
        self.assertTrue(c.lexical_strand(40, 6, 0.01, 0.15, 0.5, 13)[0])
        self.assertFalse(c.lexical_strand(40, 6, 0.03, 0.15, 0.0, 13)[0])


class MorphologyTest(unittest.TestCase):
    def test_forms_are_in_morphology_md(self):
        text = (REPO / "data" / "morphology.md").read_text(encoding="utf-8")
        for lang in c.MORPH.values():
            for forms in lang.values():
                for f in forms:
                    self.assertIn(f["form"], text)

    def test_testable_counts(self):
        self.assertEqual(c.morph_compare("ps")["testable"], 1)
        self.assertEqual(c.morph_compare("pu")["testable"], 2)
        self.assertEqual(c.morph_compare("paa")["testable"], 3)
        self.assertEqual(c.morph_compare("paa_hsed")["testable"], 0)

    def test_guttural_may_be_unaligned_in_morphology(self):
        row = c.morph_compare("paa")["items"][3]   # item 4, ai-/(n)i- ~ *ʔan-
        comp = row["comparisons"][0]
        self.assertTrue(comp["consonants_agree"])
        self.assertEqual(comp["guttural_unaligned"], "ʔ")
        self.assertFalse(comp["match"])           # position not stated


def paa_item(slot, stem, root):
    return {"slot": slot, "h_stem": stem, "ref_root": root,
            "h": c.hattic_consonants(stem), "ref": c.paa_consonants(root)}


class PaaConsonantsTest(unittest.TestCase):
    def test_first_alternative_form(self):
        self.assertEqual(phs(c.paa_consonants("*ʔaḫ- ~ *ḫaʔ-")), ["ʔ", "ḫ"])
        self.assertEqual(phs(c.paa_consonants("*baʔ-/*baw-/*bay")),
                         ["b", "ʔ"])

    def test_first_alternative_for_one_position(self):
        self.assertEqual(phs(c.paa_consonants("*naw/yl/r-")),
                         ["n", "w", "l"])
        self.assertEqual(phs(c.paa_consonants("*KVʒ/ǯVm/n/l-")),
                         ["K", "ʒ", "m"])
        self.assertEqual(phs(c.paa_consonants("*ʔi/uǯn- ~ ʔi/udn-")),
                         ["ʔ", "ǯ", "n"])

    def test_optional_segments_left_out(self):
        self.assertEqual(phs(c.paa_consonants("*sa(w/yV)ḥ-")), ["s", "ḥ"])
        self.assertEqual(phs(c.paa_consonants("*ti(m)b(-ar)-")), ["t", "b"])
        self.assertEqual(phs(c.paa_consonants("*ḳ(ʷ)as-")), ["ḳ", "s"])

    def test_affixes_left_out(self):
        self.assertEqual(phs(c.paa_consonants("*ʔa-pay-")), ["p", "y"])
        self.assertEqual(phs(c.paa_consonants("*ʔad-Vm-")), ["ʔ", "d"])
        self.assertEqual(phs(c.paa_consonants("*(ʔa-)ḫʷar-")), ["ḫʷ", "r"])
        self.assertEqual(phs(c.paa_consonants("*ʔad-Vm-", keep_affixes=True)),
                         ["ʔ", "d", "m"])

    def test_classes_by_articulation(self):
        cls = {s.ph: s.cls for s in c.paa_consonants("*ĉ̣aḳʷ-")}
        self.assertEqual(cls, {"ĉ̣": "S", "ḳʷ": "K"})
        self.assertEqual([s.cls for s in c.paa_consonants("*q̇ac̣-")],
                         ["K", "S"])
        self.assertEqual([s.cls for s in c.paa_consonants("*ᶜiĉ-")],
                         ["H", "S"])
        self.assertEqual(c.paa_class("ġ", c.PAA_CLASS), "H")  # not K
        self.assertEqual(c.paa_class("ɬ", c.PAA_CLASS), "S")  # lateral
        self.assertTrue(c.paa_consonants("*ʕVp-")[0].skippable)

    def test_geminates(self):
        self.assertEqual(phs(c.paa_consonants("*rabb-")), ["r", "b", "b"])
        self.assertEqual(phs(c.paa_consonants("*rabb-",
                                              collapse_geminates=True)),
                         ["r", "b"])

    def test_every_compared_paa_symbol_is_classed(self):
        for name in ("proto_afroasiatic.tsv", "proto_afroasiatic_hsed.tsv"):
            for r in c.read_tsv(REPO / "data" / name).values():
                if r["form"]:
                    for s in c.paa_consonants(r["form"]):
                        self.assertIsNotNone(s.cls, (name, r["slot"], s.ph))


class PaaPositiveControlTest(unittest.TestCase):
    def test_regular_paa_reflexes_are_found(self):
        # Hattic reflecting PAA regularly (*ḳ > k, *n > n, *c̣ > z, *b > p,
        # *r > l), written in PAA notation with vowels, V, a prefix and an
        # optional segment: the arm must find R >= 5 and shuffle p <= 0.01.
        roots = ["knc", "kbr", "krn", "nck", "nbr", "nrc", "ckb", "cnr",
                 "cbk", "bkn", "bcr", "brk", "rkc", "rnb", "rcn"]
        paa = {"k": "ḳ", "n": "n", "c": "c̣", "b": "b", "r": "r"}
        hat = {"k": "k", "n": "n", "c": "z", "b": "p", "r": "l"}
        items = [paa_item(i, "a".join(hat[x] for x in r) + "a",
                          "*ʔa-" + "V".join(paa[x] for x in r) + "(w)-")
                 for i, r in enumerate(roots, 1)]
        res = c.run(items)
        self.assertEqual(res["candidates"], len(roots))
        self.assertGreaterEqual(res["R"], 5)
        self.assertLessEqual(c.shuffle_control(items, res["R"])["p"], 0.01)


class CombinedReadingTest(unittest.TestCase):
    def test_a4_5_table(self):
        cd, ns, sp = "the data cannot decide", "no support", "support"
        self.assertEqual(c.combined_reading(sp, ns)[0], sp)
        self.assertEqual(c.combined_reading(ns, sp)[0], ns)
        self.assertTrue(c.combined_reading(ns, sp)[1].startswith(
            "PS-only support, PAA arm fails"))
        self.assertEqual(c.combined_reading(cd, ns)[0], ns)
        self.assertEqual(c.combined_reading(cd, cd)[0], cd)
        self.assertEqual(c.combined_reading(cd, sp)[0], cd)
        self.assertTrue(c.combined_reading(cd, sp)[1].startswith(
            "PS-only support, PAA arm cannot decide"))


class RepoTest(unittest.TestCase):
    def test_paa_arm_on_repository_data(self):
        hattic = c.read_tsv(REPO / "data" / "hattic.tsv")
        pu = c.read_tsv(REPO / "data" / "control_proto_uralic.tsv")
        counts = c.hattic_selected(hattic, "counts")
        for name, n, n2 in (("proto_afroasiatic.tsv", 17, 14),
                            ("proto_afroasiatic_hsed.tsv", 16, 14)):
            paa = c.read_tsv(REPO / "data" / name)
            res = c.evaluate(counts, paa, pu, shuffle=False, ref_kind="paa",
                             morph_kind="paa")
            self.assertEqual(res["hattic_afroasiatic"]["n"], n)
            self.assertEqual(res["hattic_uralic"]["n"], 13)
            self.assertEqual(res["outcome"], "the data cannot decide")
            res2 = c.evaluate(counts, paa, pu, shuffle=False, ref_kind="paa",
                              min_non_semitic=2)
            self.assertEqual(res2["hattic_afroasiatic"]["n"], n2)

    def test_main_run_on_repository_data(self):
        hattic = c.read_tsv(REPO / "data" / "hattic.tsv")
        ps = c.read_tsv(REPO / "data" / "proto_semitic.tsv")
        pu = c.read_tsv(REPO / "data" / "control_proto_uralic.tsv")
        res = c.evaluate(c.hattic_selected(hattic, "counts"), ps, pu,
                         shuffle=False)
        self.assertEqual(res["hattic_semitic"]["n"], 9)
        self.assertEqual(res["hattic_uralic"]["n"], 13)
        self.assertEqual(res["outcome"], "the data cannot decide")


if __name__ == "__main__":
    unittest.main()

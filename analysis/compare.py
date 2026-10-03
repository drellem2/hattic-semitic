#!/usr/bin/env python3
"""Run the pre-registered comparison (docs/preregistration.md §2-§6).

Reads data/hattic.tsv, data/proto_semitic.tsv and data/control_proto_uralic.tsv
and applies the matching rules of §3.2-§3.5 mechanically:

- consonants are read from the Hattic stem, the Proto-Semitic root and the
  Proto-Uralic form, and put into the classes of §3.2 / §4.2;
- each slot filled on both sides is aligned left to right, with at most one
  reference guttural aligned with nothing (unscored), and is a candidate if
  it has at least two scored class matches and no mismatch in its first two
  aligned positions (§3.3);
- correspondences are counted per phoneme and position over candidate pairs,
  are regular if they recur in N >= 3 independent pairs, and a candidate with
  at least two regular (unconflicted) correspondences is a regular cognate
  set; R is their number and r = R / n (§3.5);
- Control A shuffles the Hattic forms among the compared slots
  (derangements, 1000 times, seed 20261003) and re-runs everything (§4.1);
- Control B runs the identical procedure on Hattic vs Proto-Uralic (§4.2);
- the morphology items of §5 are compared by the rules of §5.2-§5.3, from the
  forms recorded in data/morphology.md, transcribed below;
- the outcome category of §6 is then read off.

Writes analysis/results.json and analysis/results.md. Exits non-zero if the
data do not validate.

Usage: python3 analysis/compare.py [repo_root]
"""

import csv
import itertools
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_data  # noqa: E402

SEED = 20261003
SHUFFLES = 1000
N_REGULAR = 3          # §3.5
MIN_N = 30             # §6
MIN_N_PU = 20          # §4.3
MORPH_MIN_TESTABLE = 4  # §5.3

CLASSES = "PMTSKNRWH"

# §3.2, Hattic column, after the §3.1 cuneiform neutralisations.
HATTIC_CLASS = {
    "p": "P", "b": "P", "v": "P", "u̯": "P",   # WA-series consonant -> P
    "m": "M", "t": "T", "d": "T",
    "s": "S", "š": "S", "z": "S",
    "k": "K", "g": "K", "n": "N", "r": "R", "l": "R",
    "i̯": "W", "y": "W", "ḫ": "H",
}
# Phoneme identity on the Hattic side after §3.1: voicing ignored, WA-series
# read as one labial.
HATTIC_PHONEME = {"b": "p", "d": "t", "g": "k", "u̯": "v", "i̯": "y"}
HATTIC_VOWELS = set("aeiou")

# §3.2, Proto-Semitic column.
PS_CLASS = {
    "p": "P", "b": "P", "m": "M", "t": "T", "d": "T", "ṭ": "T",
    "s": "S", "z": "S", "ṣ": "S", "š": "S", "ś": "S", "ṯ": "S", "ḏ": "S",
    "ṯ̣": "S", "ṱ": "S",
    "k": "K", "g": "K", "q": "K", "n": "N", "r": "R", "l": "R",
    "w": "W", "y": "W",
    "ʾ": "H", "ʿ": "H", "h": "H", "ḥ": "H", "ḫ": "H", "ġ": "H",
}

# §4.2, Proto-Uralic.
PU_CLASS = {
    "p": "P", "m": "M", "t": "T", "δ": "T", "δ́": "T",
    "s": "S", "ś": "S", "š": "S", "č": "S", "ć": "S",
    "k": "K", "n": "N", "ń": "N", "ŋ": "N",
    "r": "R", "l": "R", "ľ": "R", "w": "W", "j": "W", "x": "H",
}
PU_VOWELS = set("aeiouäåüöɨɜȣēāīōū")

# A4.4, Proto-Afroasiatic, by articulation. Graphemes as the two PAA sources
# write them; ˀ, ˁ and ᶜ are the A6 transcriptions of HSED's raised hooks for
# the glottal stop and ʿayin. A grapheme not listed here is looked up again
# with the glottalisation/emphasis marks (dot below, dot above) and the
# labialisation mark ʷ removed, which puts glottalised, emphatic and
# labialised consonants into the class of their plain counterpart (A4.4).
PAA_CLASS = {
    "p": "P", "b": "P", "f": "P",
    "m": "M",
    "t": "T", "d": "T",
    "s": "S", "z": "S", "š": "S", "c": "S", "ʒ": "S", "č": "S", "ǯ": "S",
    "ĉ": "S", "ś": "S", "ŝ": "S", "ɬ": "S", "ł": "S", "ṯ": "S", "ḏ": "S",
    "k": "K", "g": "K", "q": "K",
    "n": "N", "ñ": "N", "ŋ": "N",
    "r": "R", "l": "R",
    "w": "W", "y": "W", "j": "W",
    "ʔ": "H", "ʕ": "H", "h": "H", "ḥ": "H", "ħ": "H", "x": "H", "ḫ": "H",
    "ɣ": "H", "ġ": "H", "ˀ": "H", "ˁ": "H", "ᶜ": "H",
}
PAA_VOWELS = set("aeiouüəV")
PAA_MARKS = ("̣", "̇", "ʷ")   # dot below, dot above, labialised

# Symbols in the data that the class tables of §3.2 / §4.2 do not list.
# The class given here is the analyst's reading, fixed before the first run;
# `inferred_symbol_sensitivity` re-runs the comparison under every possible
# class for each of them (including "matches nothing"), and the results
# report whether any candidate decision changes.
INFERRED = {
    "hattic": {"h": "H"},     # plain h in a stem written ḫ in the text
    "ps": {
        "x̣": "H",             # AHD letter; roots for carry, see, sweet
        "ṣ́": "S",             # emphatic lateral sibilant (ṣ series)
    },
    "pu": {"c": "S", "d": "T", "γ": "H"},
    # Capital H and K are the PAA sources' cover symbols for "a laryngeal"
    # and "a velar" of unknown identity (A4.4 does not list them).
    "paa": {"H": "H", "K": "K"},
}
GUTTURAL = "H"


def graphemes(s):
    """Split into base letters with their combining marks attached."""
    out = []
    for ch in unicodedata.normalize("NFC", s):
        if out and unicodedata.combining(ch):
            out[-1] += ch
        else:
            out.append(ch)
    return out


class Seg:
    """One consonant: phoneme as compared, its class, and whether it is a
    reference-side guttural that may be aligned with nothing."""

    __slots__ = ("ph", "cls", "skippable")

    def __init__(self, ph, cls, skippable=False):
        self.ph, self.cls, self.skippable = ph, cls, skippable

    def __repr__(self):
        return f"{self.ph}:{self.cls or '?'}"


def hattic_consonants(stem, classes=None):
    """Consonants of a Hattic stem (§3.1). Of `a/b` alternatives the first is
    taken; parenthesised letters are spelling variants and are read; doubled
    writing is read as single."""
    classes = classes or {**HATTIC_CLASS, **INFERRED["hattic"]}
    stem = stem.split("/")[0]
    letters = [g for g in graphemes(stem) if g not in "()-*"]
    out, prev = [], None
    for g in letters:
        base = g
        if base[0] in HATTIC_VOWELS and base not in ("u̯", "i̯"):
            prev = None
            continue
        if base == prev:          # doubled writing read as single
            continue
        prev = base
        out.append(Seg(HATTIC_PHONEME.get(base, base), classes.get(base)))
    return out


def ps_consonants(root, classes=None):
    """Root consonants of a Proto-Semitic root, in order (§3.1); homograph
    numbers are dropped."""
    classes = classes or {**PS_CLASS, **INFERRED["ps"]}
    out = []
    for g in graphemes(root):
        if g.isdigit():
            continue
        c = classes.get(g)
        out.append(Seg(g, c, c == GUTTURAL))
    return out


def pu_consonants(form, classes=None, collapse_geminates=False):
    """Consonants of a Proto-Uralic form (§4.2). Of several forms in a cell
    the first is taken; `/` marks a vowel alternation inside one form."""
    classes = classes or {**PU_CLASS, **INFERRED["pu"]}
    first = form.split(" (")[0].split(", ")[0]
    out, prev = [], None
    for g in graphemes(first):
        if g in "*-/()":
            continue
        if g[0] in PU_VOWELS:
            prev = None
            continue
        if collapse_geminates and g == prev:
            continue
        prev = g
        c = classes.get(g)
        out.append(Seg(g, c, c == GUTTURAL))
    return out


def paa_class(g, classes):
    """A4.4 class of one PAA grapheme, or None if it cannot be placed."""
    if g in classes:
        return classes[g]
    base = unicodedata.normalize("NFD", g)
    for mark in PAA_MARKS:
        base = base.replace(mark, "")
    return classes.get(unicodedata.normalize("NFC", base))


def paa_root_chunk(form):
    """Drop what the source marks as an affix or root extension (A4.4): in
    both PAA sources a hyphen inside a reconstruction separates morphemes
    (*ʔa-pay-, *ḥar-Vk-, *ʔad-Vm-). The root is the first hyphen-delimited
    part with at least two consonants, else the first with any."""
    parts = [p for p in form.split("-") if p]
    if len(parts) <= 1:
        return "".join(parts)

    def n_cons(p):
        return sum(1 for g in graphemes(p)
                   if g not in PAA_VOWELS and g not in "/")
    for k in (2, 1):
        for p in parts:
            if n_cons(p) >= k:
                return p
    return parts[0]


def paa_consonants(form, classes=None, keep_affixes=False,
                   collapse_geminates=False):
    """Consonants of a PAA reconstruction (A4.4), in the source's notation.

    Of alternative forms (`~`, or `/` between starred forms) the first is
    taken; parenthesised (optional) segments are left out; of alternatives
    for one position (`w/y`) the first-listed is used; affixes and root
    extensions marked by an internal hyphen are left out (`paa_root_chunk`);
    vowels, including the cover vowel V, are not compared."""
    classes = classes or {**PAA_CLASS, **INFERRED["paa"]}
    f = unicodedata.normalize("NFC", form).split("~")[0].strip()
    f = f.split("/*")[0]
    while True:
        g = re.sub(r"\([^()]*\)", "", f)
        if g == f:
            break
        f = g
    f = f.replace("*", "").strip()
    if not keep_affixes:
        f = paa_root_chunk(f)
    gs = []
    for g in graphemes(f):
        if g == "ʷ" and gs:
            gs[-1] += g
        else:
            gs.append(g)
    out, prev, skip_next = [], None, False
    for g in gs:
        if skip_next:
            skip_next = False
            continue
        if g == "/":
            skip_next = True
            continue
        if g == "-":
            continue
        if g in PAA_VOWELS:
            prev = None
            continue
        if collapse_geminates and g == prev:
            continue
        prev = g
        c = paa_class(g, classes)
        out.append(Seg(g, c, c == GUTTURAL))
    return out


def class_match(a, b):
    if a is None or b is None:
        return False
    return a == b or {a, b} == {"T", "S"}


def align(h, ref):
    """Best alignment of Hattic consonants `h` with reference consonants
    `ref` under §3.3. Returns a dict with the aligned positions, the number of
    scored matches, whether the pair is a candidate, and which reference
    guttural (if any) was aligned with nothing."""
    options = [None] + [j for j, s in enumerate(ref) if s.skippable]
    best = None
    for skip in options:
        ref_idx = [j for j in range(len(ref)) if j != skip]
        positions = []
        for hs, j in zip(h, ref_idx):
            rs = ref[j]
            positions.append({
                "ref": rs.ph, "ref_cls": rs.cls, "hattic": hs.ph,
                "hattic_cls": hs.cls,
                "position": "initial" if j == 0 else "non-initial",
                "match": class_match(hs.cls, rs.cls),
            })
        matches = sum(p["match"] for p in positions)
        first_two_ok = all(p["match"] for p in positions[:2])
        candidate = len(h) >= 2 and matches >= 2 and first_two_ok
        key = (candidate, matches, skip is None, -(skip or 0))
        if best is None or key > best[0]:
            best = (key, {"positions": positions, "matches": matches,
                          "candidate": candidate,
                          "skipped": None if skip is None else ref[skip].ph})
    return best[1]


def max_independent(pairs):
    """Largest set of pairs no two of which share a Hattic stem or a
    reference root (§3.5): a maximum bipartite matching."""
    match_of_root = {}

    def try_assign(stem, seen):
        for root in adj[stem]:
            if root in seen:
                continue
            seen.add(root)
            if root not in match_of_root or try_assign(match_of_root[root], seen):
                match_of_root[root] = stem
                return True
        return False

    adj = {}
    for stem, root in pairs:
        adj.setdefault(stem, []).append(root)
    return sum(try_assign(stem, set()) for stem in adj)


def run(items):
    """Run §3.3-§3.5 on a list of slot items, each a dict with slot, h_stem,
    ref_root and the consonant lists `h` and `ref`."""
    pairs = []
    for it in items:
        a = align(it["h"], it["ref"])
        pairs.append({**{k: it[k] for k in ("slot", "h_stem", "ref_root")},
                      "monoconsonantal": len(it["h"]) < 2, **a})
    cands = [p for p in pairs if p["candidate"]]

    corr = {}
    for p in cands:
        for pos in p["positions"]:
            key = (pos["ref"], pos["hattic"], pos["position"])
            corr.setdefault(key, []).append(p)
    table = []
    for key, sup in sorted(corr.items()):
        indep = max_independent({(p["h_stem"], p["ref_root"]) for p in sup})
        table.append({"ref": key[0], "hattic": key[1], "position": key[2],
                      "support_slots": sorted({p["slot"] for p in sup}),
                      "independent": indep,
                      "regular": indep >= N_REGULAR})

    # Consistency (§3.5): one reflex per reference phoneme and position, unless
    # a conditioning environment is stated. The data state none, so every
    # competing regular reflex beyond the most frequent is unconditioned.
    primary = {}
    for c in sorted((c for c in table if c["regular"]),
                    key=lambda c: (-c["independent"], -len(c["support_slots"]),
                                   c["hattic"])):
        primary.setdefault((c["ref"], c["position"]), c["hattic"])
    for c in table:
        c["unconditioned_competitor"] = (
            c["regular"] and primary[(c["ref"], c["position"])] != c["hattic"])
    usable = {(c["ref"], c["hattic"], c["position"]) for c in table
              if c["regular"] and not c["unconditioned_competitor"]}

    for p in pairs:
        n_reg = sum((q["ref"], q["hattic"], q["position"]) in usable
                    for q in p["positions"]) if p["candidate"] else 0
        p["regular_correspondences"] = n_reg
        p["regular_cognate_set"] = n_reg >= 2
    R = sum(p["regular_cognate_set"] for p in pairs)
    n = len(items)
    return {"n": n, "R": R, "r": R / n if n else None,
            "candidates": len(cands), "pairs": pairs,
            "correspondences": table}


def read_tsv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return {int(r["slot"]): r for r in
                csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)}


def hattic_selected(hattic, mode):
    """Hattic rows entering a run.

    counts      - cited and secure (§1.2), the decision set under A3
    collated    - as `counts`, with `uncollated` forms excluded explicitly
    exploratory - every filled lexical slot with a stem, doubtful included
    strict      - forms cited from Soysal 2004, the source §7.2 names (A3)
    """
    out = {}
    for s, r in hattic.items():
        if r["strand"] != "lexical" or not r["form"] or not r["stem"]:
            continue
        cited = r["provenance"].startswith("cited:")
        if mode in ("counts", "collated") and r["decision"] != "counts":
            continue
        if mode == "collated" and not cited:
            continue
        if mode == "strict" and not (cited and "Soysal" in r["provenance"]
                                     and r["decision"] == "counts"):
            continue
        out[s] = r
    return out


def build_items(hrows, ref, ref_kind, exact_only=False, classes=None,
                collapse_geminates=False, min_non_semitic=0,
                keep_affixes=False):
    classes = classes or {}
    items = []
    for s in sorted(hrows):
        rr = ref.get(s)
        if not rr or not rr["form"]:
            continue
        if exact_only and "permitted-shift" in (hrows[s]["match"], rr["match"]):
            continue
        if (min_non_semitic
                and int(rr["non_semitic_branches"]) < min_non_semitic):
            continue
        if ref_kind == "ps":
            root = rr["root"]
            refc = ps_consonants(root, classes.get("ps"))
        elif ref_kind == "paa":
            root = rr["form"]
            refc = paa_consonants(root, classes.get("paa"), keep_affixes,
                                  collapse_geminates)
        else:
            root = rr["form"]
            refc = pu_consonants(root, classes.get("pu"), collapse_geminates)
        items.append({"slot": s, "h_stem": hrows[s]["stem"], "ref_root": root,
                      "h": hattic_consonants(hrows[s]["stem"],
                                             classes.get("hattic")),
                      "ref": refc})
    return items


def derangement(rng, n):
    idx = list(range(n))
    while True:
        rng.shuffle(idx)
        if all(i != j for i, j in enumerate(idx)):
            return idx


def shuffle_control(items, observed_R, seed=SEED, times=SHUFFLES):
    """Control A (§4.1)."""
    rng = random.Random(seed)
    dist = []
    if len(items) >= 2:
        for _ in range(times):
            perm = derangement(rng, len(items))
            shuffled = [{**it, "h": items[perm[k]]["h"],
                         "h_stem": items[perm[k]]["h_stem"]}
                        for k, it in enumerate(items)]
            dist.append(run(shuffled)["R"])
    ge = sum(d >= observed_R for d in dist)
    p = (1 + ge) / (1 + times) if dist else None
    hist = {}
    for d in dist:
        hist[d] = hist.get(d, 0) + 1
    return {"p": p, "shuffles": len(dist), "ge_observed": ge,
            "distribution": dict(sorted(hist.items()))}


# §5.1 forms, transcribed from data/morphology.md. Only cited, securely
# glossed forms are listed (an item is testable only if both sides have one).
# `cons` are the form's consonants read as in §3.1/§3.2.
MORPH = {
    "hattic": {
        2: [{"form": "ú-un", "position": "independent", "cons": ["n"]},
            {"form": "ú-/u-", "position": "prefix", "cons": []}],
        3: [{"form": "li-e- (lē-)", "position": "prefix", "cons": ["l"]},
            {"form": "te-", "position": "prefix", "cons": ["t"]},
            {"form": "le-", "position": "prefix", "cons": ["l"]},
            {"form": "-e, -i̯a", "position": "suffix", "cons": []}],
        4: [{"form": "ai- / (n)i-", "position": "prefix", "cons": ["n"]}],
        5: [{"form": "taš- (teš-)", "position": "prefix", "cons": ["t", "š"]}],
        6: [{"form": "taš-te-", "position": "prefix",
             "cons": ["t", "š", "t"]}],
        7: [{"form": "u̯aₐ-", "position": "prefix", "cons": ["v"]},
            {"form": "eš-", "position": "prefix", "cons": ["š"]}],
    },
    "ps": {
        1: [{"form": "*-ī/-ya", "position": "suffix", "cons": ["y"]}],
        4: [{"form": "*-na/-ni/-nu", "position": "suffix", "cons": ["n"]}],
    },
    "pu": {
        1: [{"form": "mȣ̈", "position": "independent", "cons": ["m"]}],
        2: [{"form": "*tun", "position": "independent", "cons": ["t", "n"]}],
        4: [{"form": "mȣ̈", "position": "independent", "cons": ["m"]}],
    },
    # A4.1/A5 rule 7: the Militarev-Stolbova database. It does not say
    # whether a form is bound or independent, so position is "not stated".
    "paa": {
        1: [{"form": "*-aku", "position": "not stated", "cons": ["k"]},
            {"form": "*ʔan-", "position": "not stated", "cons": ["ʔ", "n"]}],
        2: [{"form": "*ʔan-", "position": "not stated", "cons": ["ʔ", "n"]}],
        4: [{"form": "*ʔan-", "position": "not stated", "cons": ["ʔ", "n"]}],
        5: [{"form": "*ʔVl-", "position": "not stated", "cons": ["ʔ", "l"]},
            {"form": "*ʔy-", "position": "not stated", "cons": ["ʔ", "y"]},
            {"form": "*ma", "position": "not stated", "cons": ["m"]}],
    },
    # A6 rule 11: HSED gives none of the eight items.
    "paa_hsed": {},
}
UNSTATED = "not stated"
MORPH_ITEMS = {1: "1sg", 2: "2sg", 3: "3sg", 4: "1pl", 5: "negation",
               6: "prohibitive", 7: "nominal plural", 8: "causative"}


def morph_compare(ref_kind):
    """§5.2-§5.3 for Hattic vs `ref_kind`. No regular correspondence exists
    (R = 0 in every run), so consonants agree by class match, aligned left to
    right as in §3.3, with at most one reference guttural aligned with
    nothing (§3.2). A reference form whose position the source does not state
    cannot be shown to agree in position, so its match is not counted."""
    hcls = {**HATTIC_CLASS, **INFERRED["hattic"]}
    if ref_kind == "ps":
        rcls = {**PS_CLASS, **INFERRED["ps"]}.get
    elif ref_kind == "pu":
        rcls = {**PU_CLASS, **INFERRED["pu"]}.get
    else:
        allp = {**PAA_CLASS, **INFERRED["paa"]}
        rcls = lambda g: paa_class(g, allp)  # noqa: E731
    rows, cell_matches = [], []
    for item, name in MORPH_ITEMS.items():
        hs = MORPH["hattic"].get(item, [])
        rs = MORPH[ref_kind].get(item, [])
        testable = bool(hs and rs)
        comps = []
        for h, r in itertools.product(hs, rs):
            same_pos = h["position"] == r["position"]
            best = None
            skips = [None] + [j for j, x in enumerate(r["cons"])
                              if rcls(x) == GUTTURAL]
            for skip in skips:
                rc = [x for j, x in enumerate(r["cons"]) if j != skip]
                aligned = list(zip(h["cons"], rc))
                agree = bool(aligned) and all(
                    class_match(hcls.get(a), rcls(b)) for a, b in aligned)
                key = (agree, len(aligned) if agree else 0, skip is None)
                if best is None or key > best[0]:
                    best = (key, agree, len(aligned) if agree else 0,
                            None if skip is None else r["cons"][skip])
            _, cons_agree, n_cons, skipped = best
            match = same_pos and cons_agree
            comp = {"hattic": h["form"], "ref": r["form"],
                    "hattic_position": h["position"],
                    "ref_position": r["position"],
                    "position_agrees": same_pos,
                    "consonants_agree": cons_agree,
                    "matching_consonants": n_cons, "match": match}
            if skipped is not None:
                comp["guttural_unaligned"] = skipped
            comps.append(comp)
            if match:
                cell_matches.append((item, h["position"], n_cons))
        rows.append({"item": item, "name": name, "testable": testable,
                     "comparisons": comps})
    nontrivial = sum(1 for _, _, k in cell_matches if k >= 2)
    # paradigm match: >= 2 of items 1-4 matching in one position series,
    # counted once, and only if those cells are not already non-trivial
    by_series = {}
    for item, pos, k in cell_matches:
        if item <= 4 and k < 2:
            by_series.setdefault(pos, set()).add(item)
    nontrivial += sum(1 for s in by_series.values() if len(s) >= 2)
    return {"items": rows, "testable": sum(r["testable"] for r in rows),
            "nontrivial": nontrivial}


def lexical_strand(n, R, p, r, r_pu, n_pu):
    """§4.3. Returns (passes, conditions)."""
    conds = {"R>=5": R >= 5}
    if n_pu < MIN_N_PU:
        conds["control B uninformative (n_PU < 20)"] = True
        conds["p<=0.01"] = p is not None and p <= 0.01
    else:
        conds["p<=0.05"] = p is not None and p <= 0.05
        conds["r>=2*r_PU and r-r_PU>=0.05"] = (
            r is not None and r_pu is not None
            and r >= 2 * r_pu and r - r_pu >= 0.05)
    passes = all(v for k, v in conds.items() if not k.startswith("control B"))
    return passes, conds


def outcome(n, lex_pass, morph_testable, morph_pass):
    """§6, read off mechanically."""
    if n < MIN_N:
        return "the data cannot decide", f"n = {n} < {MIN_N}"
    if not lex_pass:
        return "no support", "n >= 30 and the lexical strand fails"
    if not morph_testable:
        return ("the data cannot decide",
                "lexical strand passes; morphology strand not testable")
    if not morph_pass:
        return ("the data cannot decide",
                "lexical strand passes; morphology strand fails")
    return "support", "lexical and morphology strands pass"


ARM_KEY = {"ps": "hattic_semitic", "paa": "hattic_afroasiatic"}


def evaluate(hrows, ref, pu, exact_only=False, classes=None,
             collapse_geminates=False, shuffle=True, ref_kind="ps",
             morph_kind=None, min_non_semitic=0, keep_affixes=False):
    """One run of one arm: Hattic vs `ref` (Proto-Semitic, or for the A4
    arm Proto-Afroasiatic), with Control A on that arm and Control B
    (Hattic vs Proto-Uralic, the same for both arms, A4.3)."""
    key = ARM_KEY[ref_kind]
    morph_kind = morph_kind or ref_kind
    items_ref = build_items(hrows, ref, ref_kind, exact_only, classes,
                            collapse_geminates, min_non_semitic, keep_affixes)
    items_pu = build_items(hrows, pu, "pu", exact_only, classes,
                           collapse_geminates)
    res_ref = run(items_ref)
    res_pu = run(items_pu)
    ctl = (shuffle_control(items_ref, res_ref["R"]) if shuffle
           else {"p": None})
    m_ref, m_pu = morph_compare(morph_kind), morph_compare("pu")
    lex_pass, conds = lexical_strand(res_ref["n"], res_ref["R"], ctl["p"],
                                     res_ref["r"], res_pu["r"], res_pu["n"])
    morph_testable = m_ref["testable"] >= MORPH_MIN_TESTABLE
    morph_pass = (morph_testable and m_ref["nontrivial"] >= 2
                  and m_ref["nontrivial"] - m_pu["nontrivial"] >= 2)
    cat, why = outcome(res_ref["n"], lex_pass, morph_testable, morph_pass)
    return {key: res_ref, "hattic_uralic": res_pu,
            "control_A": ctl, "lexical_conditions": conds,
            "lexical_pass": lex_pass,
            "morphology": {key: m_ref, "hattic_uralic": m_pu,
                           "testable": morph_testable, "pass": morph_pass},
            "outcome": cat, "outcome_reason": why}


def combined_reading(paa, ps):
    """A4.5: only the PAA arm can give support to the sister reading."""
    if paa == "support":
        return "support", f"PAA arm supports; PS arm: {ps}"
    if paa == "no support":
        lead = ("PS-only support, PAA arm fails; "
                if ps == "support" else "")
        return "no support", lead + "PAA arm: no support"
    if ps == "no support":
        return "no support", ("PAA arm cannot decide; the PS arm's "
                              "no support stands")
    lead = ("PS-only support, PAA arm cannot decide; "
            if ps == "support" else "")
    return ("the data cannot decide",
            lead + f"PAA arm cannot decide; PS arm: {ps}")


def signature(result, key="hattic_semitic"):
    """What a re-run could change: candidacy per slot, R, and the outcome."""
    return {"candidates": [(k, p["slot"]) for k in (key, "hattic_uralic")
                           for p in result[k]["pairs"] if p["candidate"]],
            "R": result[key]["R"],
            "R_PU": result["hattic_uralic"]["R"],
            "outcome": result["outcome"]}


def inferred_symbol_sensitivity(hrows, ref, pu, ref_kind="ps",
                                morph_kind=None):
    """Re-run with every inferred symbol (INFERRED) set, one at a time, to
    every class and to 'matches nothing'; also with Proto-Uralic geminates
    read as one consonant (and, for the PAA arm, PAA geminates read as one
    and PAA affixes kept). Return every re-run whose candidates, R, R_PU or
    outcome differ from the run as read."""
    key = ARM_KEY[ref_kind]
    kw0 = {"ref_kind": ref_kind, "morph_kind": morph_kind}
    base = signature(evaluate(hrows, ref, pu, shuffle=False, **kw0), key)
    changed = []
    variants = []
    sides = ("hattic", ref_kind, "pu")
    for side in sides:
        for sym in INFERRED[side]:
            for cls in list(CLASSES) + [None]:
                classes = {
                    "hattic": {**HATTIC_CLASS, **INFERRED["hattic"]},
                    "ps": {**PS_CLASS, **INFERRED["ps"]},
                    "pu": {**PU_CLASS, **INFERRED["pu"]},
                    "paa": {**PAA_CLASS, **INFERRED["paa"]},
                }
                if cls is None:
                    classes[side].pop(sym)
                else:
                    classes[side][sym] = cls
                variants.append((f"{side} {sym} -> {cls or 'nothing'}",
                                 {"classes": classes}))
    if ref_kind == "paa":
        variants.append(("Proto-Uralic and PAA geminates read as single",
                         {"collapse_geminates": True}))
        variants.append(("PAA affixes and root extensions kept",
                         {"keep_affixes": True}))
    else:
        variants.append(("Proto-Uralic geminates read as single",
                         {"collapse_geminates": True}))
    for label, kw in variants:
        sig = signature(evaluate(hrows, ref, pu, shuffle=False, **kw0, **kw),
                        key)
        if sig != base:
            changed.append({"variant": label,
                            **{k: sig[k] for k in sig if sig[k] != base[k]}})
    return {"runs": len(variants), "changed": changed}


def fmt_r(x):
    return "—" if x is None else f"{x:.3f}"


def pair_line(p):
    al = " ".join(
        f"{q['ref']}~{q['hattic']}{'+' if q['match'] else '×'}"
        for q in p["positions"]) or "(nothing aligned)"
    skip = f"; {p['skipped']}~∅ unscored" if p["skipped"] else ""
    if p["monoconsonantal"]:
        verdict = "monoconsonantal Hattic stem: listed, never scored (§3.3)"
    else:
        verdict = "**candidate**" if p["candidate"] else "not a candidate"
    return (f"| {p['slot']} | {p['h_stem']} | {p['ref_root']} | {al}{skip} | "
            f"{p['matches']} | {verdict} |")


def render(results, meanings):
    L = []
    L.append("# Comparison output")
    L.append("")
    L.append("Generated by `python3 analysis/compare.py` from `data/`. Do not "
             "edit by hand; the summary is in "
             "[`../results/summary.md`](../results/summary.md).")
    L.append("")
    L.append("Alignment notation: `ref~hattic` per aligned position, `+` a "
             "class match (§3.2), `×` a mismatch; `X~∅` a reference guttural "
             "aligned with nothing (unscored).")
    for name, key in (("Main run (A3, cited + secure Hattic forms)", "main"),
                      ("Collated-only (uncollated forms excluded)",
                       "collated"),
                      ("`exact` pairs only (§2 sensitivity)", "exact"),
                      ("Exploratory (doubtful Hattic glosses included; "
                       "not part of the decision)", "exploratory"),
                      ("Strict reading of §1.1 (Soysal 2004 only)",
                       "strict")):
        res = results["runs"][key]
        L.append("")
        L.append(f"## {name}")
        L.append("")
        L.append(f"Outcome category (§6): **{res['outcome']}** "
                 f"({res['outcome_reason']}).")
        L.append("")
        hs, hu = res["hattic_semitic"], res["hattic_uralic"]
        ctl = res["control_A"]
        L.append("| | Hattic–Proto-Semitic | Hattic–Proto-Uralic (Control B) |")
        L.append("|---|---|---|")
        L.append(f"| n (slots compared) | {hs['n']} | {hu['n']} |")
        L.append(f"| candidates (§3.3) | {hs['candidates']} | "
                 f"{hu['candidates']} |")
        L.append(f"| R (regular cognate sets) | {hs['R']} | {hu['R']} |")
        L.append(f"| r = R / n | {fmt_r(hs['r'])} | {fmt_r(hu['r'])} |")
        p = "—" if ctl["p"] is None else f"{ctl['p']:.3f}"
        L.append(f"| Control A shuffle p | {p} | not run (§4.1 is "
                 f"Hattic–Semitic only) |")
        if ctl.get("shuffles"):
            L.append("")
            L.append(f"Control A: {ctl['shuffles']} derangements, seed "
                     f"{SEED}; R_shuffle distribution "
                     f"{ctl['distribution']}; shuffles with R_shuffle ≥ "
                     f"R_observed: {ctl['ge_observed']}.")
        L.append("")
        L.append("Lexical criterion (§4.3): " + "; ".join(
            f"{k}: {'yes' if v else 'no'}"
            for k, v in res["lexical_conditions"].items())
                 + f" → strand {'passes' if res['lexical_pass'] else 'fails'}.")
        if key not in ("main", "exploratory"):
            continue
        for label, r in (("Hattic–Proto-Semitic", hs),
                         ("Hattic–Proto-Uralic", hu)):
            L.append("")
            L.append(f"### {label}: every compared slot")
            L.append("")
            L.append("| slot | Hattic stem | reference | alignment | "
                     "matches | result |")
            L.append("|---|---|---|---|---|---|")
            for q in r["pairs"]:
                L.append(pair_line(q).replace(
                    f"| {q['slot']} |",
                    f"| {q['slot']} {meanings[q['slot']]} |", 1))
            L.append("")
            if r["correspondences"]:
                L.append("Correspondences in candidate pairs:")
                L.append("")
                L.append("| reference | Hattic | position | slots | "
                         "independent | regular |")
                L.append("|---|---|---|---|---|---|")
                for c in r["correspondences"]:
                    L.append(f"| {c['ref']} | {c['hattic']} | {c['position']}"
                             f" | {c['support_slots']} | {c['independent']} | "
                             f"{'yes' if c['regular'] else 'no'} |")
            else:
                L.append("No candidate pairs, so no correspondence sets and "
                         "no correspondence recurs at all (N ≥ 3 needed).")
    L.append("")
    L.append("## Morphology (§5)")
    m = results["runs"]["main"]["morphology"]
    for label, k in (("Hattic–Proto-Semitic", "hattic_semitic"),
                     ("Hattic–Proto-Uralic", "hattic_uralic")):
        mm = m[k]
        L.append("")
        L.append(f"### {label}: {mm['testable']} of 8 items testable; "
                 f"{mm['nontrivial']} non-trivial matches")
        L.append("")
        L.append("| item | testable | Hattic | reference | position | "
                 "consonants | match |")
        L.append("|---|---|---|---|---|---|---|")
        for row in mm["items"]:
            if not row["comparisons"]:
                L.append(f"| {row['item']} {row['name']} | no | | | | | |")
            for c in row["comparisons"]:
                pos = ("agree" if c["position_agrees"] else
                       f"differ ({c['hattic_position']} vs "
                       f"{c['ref_position']}), not counted")
                cons = ("agree" if c["consonants_agree"] else "differ")
                L.append(f"| {row['item']} {row['name']} | "
                         f"{'yes' if row['testable'] else 'no'} | "
                         f"{c['hattic']} | {c['ref']} | {pos} | {cons} | "
                         f"{'yes' if c['match'] else 'no'} |")
    L.append("")
    L.append(f"Morphology strand (§5.3): "
             f"{'testable' if m['testable'] else 'not testable'} "
             f"(needs ≥ {MORPH_MIN_TESTABLE} testable items); "
             f"{'passes' if m['pass'] else 'does not pass'}.")
    L.append("")
    L.append("## Symbols the class tables do not list")
    L.append("")
    L.append("Read as: " + "; ".join(
        f"{side} {s} → {c}" for side, d in INFERRED.items()
        if side in ("hattic", "ps", "pu") for s, c in d.items()) + ".")
    sens = results["sensitivity"]
    L.append("")
    L.append(f"Each was re-run under every class and under \"matches "
             f"nothing\", and Proto-Uralic geminates were also read as "
             f"single ({sens['runs']} re-runs, on the exploratory set, which "
             f"contains every compared slot). " + (
                 "R, R_PU and the outcome category are unchanged in every "
                 "re-run." if not any(
                     k in c for c in sens["changed"]
                     for k in ("R", "R_PU", "outcome"))
                 else "**R, R_PU or the outcome changes in at least one "
                      "re-run; see below.**"))
    if sens["changed"]:
        L.append("")
        L.append("Re-runs in which a candidate decision differs:")
        L.append("")
        for c in sens["changed"]:
            extra = {k: v for k, v in c.items() if k != "variant"}
            L.append(f"- {c['variant']}: {extra}")
    L.append("")
    return "\n".join(L)


PAA_SOURCES = (
    ("primary", "proto_afroasiatic.tsv", "paa",
     "Primary source: Militarev & Stolbova database (A4.1, A5)"),
    ("hsed", "proto_afroasiatic_hsed.tsv", "paa_hsed",
     "Sensitivity source: Orel & Stolbova 1995, HSED (A4.1, A6) — "
     "never decisive"),
)
PAA_RUNS = (
    ("main", "Main run (A3 Hattic forms: cited + secure)"),
    ("collated", "Collated-only (uncollated forms excluded)"),
    ("exact", "`exact` pairs only (§2 sensitivity)"),
    ("nonsem2", "PAA forms with at least two non-Semitic branches (A4.1)"),
    ("exploratory", "Exploratory (doubtful Hattic glosses included; "
                    "not part of the decision)"),
    ("strict", "Strict reading of §1.1 (Soysal 2004 only)"),
)


def paa_arm(hattic, paa, pu, morph_kind):
    """Every run A4 and §6.2 ask for, on one PAA list."""
    kw = {"ref_kind": "paa", "morph_kind": morph_kind}
    counts = hattic_selected(hattic, "counts")
    runs = {
        "main": evaluate(counts, paa, pu, **kw),
        "collated": evaluate(hattic_selected(hattic, "collated"), paa, pu,
                             **kw),
        "exact": evaluate(counts, paa, pu, exact_only=True, **kw),
        "nonsem2": evaluate(counts, paa, pu, min_non_semitic=2, **kw),
        "exploratory": evaluate(hattic_selected(hattic, "exploratory"),
                                paa, pu, **kw),
        "strict": evaluate(hattic_selected(hattic, "strict"), paa, pu, **kw),
    }
    return {"runs": runs,
            "sensitivity": inferred_symbol_sensitivity(
                hattic_selected(hattic, "exploratory"), paa, pu, "paa",
                morph_kind)}


def render_paa(results, meanings):
    K = ARM_KEY["paa"]
    L = ["# Comparison output: the Proto-Afroasiatic arm (A4)", ""]
    L.append("Generated by `python3 analysis/compare.py` from `data/`. Do not "
             "edit by hand; the summary is in "
             "[`../results/summary.md`](../results/summary.md). The "
             "Proto-Semitic arm is in [`results.md`](results.md).")
    L.append("")
    L.append("Alignment notation: `ref~hattic` per aligned position, `+` a "
             "class match (§3.2, A4.4), `×` a mismatch; `X~∅` a reference "
             "guttural aligned with nothing (unscored). The PAA consonants "
             "are those read from the reconstruction by A4.4: first of "
             "alternative forms, optional (parenthesised) segments left out, "
             "first-listed of alternatives for one position, affixes marked "
             "by an internal hyphen left out, vowels (including V) not "
             "compared.")
    cr = results["combined"]
    L.append("")
    L.append(f"**PAA arm (primary source): {results['primary']['runs']['main']['outcome']}.** "
             f"PS arm (mg-462a2, unchanged): {results['ps_outcome']}. "
             f"**Combined reading (A4.5): {cr['reading']}** ({cr['reason']}).")
    for src, _, _, title in PAA_SOURCES:
        arm = results[src]
        L.append("")
        L.append(f"# {title}")
        for key, name in PAA_RUNS:
            res = arm["runs"][key]
            ha, hu = res[K], res["hattic_uralic"]
            ctl = res["control_A"]
            L.append("")
            L.append(f"## {name}")
            L.append("")
            L.append(f"Outcome category (§6, A4.2): **{res['outcome']}** "
                     f"({res['outcome_reason']}).")
            L.append("")
            L.append("| | Hattic–Proto-Afroasiatic | "
                     "Hattic–Proto-Uralic (Control B) |")
            L.append("|---|---|---|")
            L.append(f"| n (slots compared) | {ha['n']} | {hu['n']} |")
            L.append(f"| candidates (§3.3) | {ha['candidates']} | "
                     f"{hu['candidates']} |")
            L.append(f"| R (regular cognate sets) | {ha['R']} | {hu['R']} |")
            L.append(f"| r = R / n | {fmt_r(ha['r'])} | {fmt_r(hu['r'])} |")
            p = "—" if ctl["p"] is None else f"{ctl['p']:.3f}"
            L.append(f"| Control A shuffle p | {p} | not run (A4.3: "
                     f"Hattic–PAA only) |")
            if ctl.get("shuffles"):
                L.append("")
                L.append(f"Control A: {ctl['shuffles']} derangements, seed "
                         f"{SEED}; R_shuffle distribution "
                         f"{ctl['distribution']}; shuffles with R_shuffle ≥ "
                         f"R_observed: {ctl['ge_observed']}.")
            L.append("")
            L.append("Lexical criterion (§4.3, A4.3): " + "; ".join(
                f"{k}: {'yes' if v else 'no'}"
                for k, v in res["lexical_conditions"].items())
                     + f" → strand "
                       f"{'passes' if res['lexical_pass'] else 'fails'}.")
            if key not in ("main", "exploratory"):
                continue
            L.append("")
            L.append("### Hattic–Proto-Afroasiatic: every compared slot")
            L.append("")
            L.append("| slot | Hattic stem | reference | alignment | "
                     "matches | result |")
            L.append("|---|---|---|---|---|---|")
            for q in ha["pairs"]:
                L.append(pair_line(q).replace(
                    f"| {q['slot']} |",
                    f"| {q['slot']} {meanings[q['slot']]} |", 1))
            L.append("")
            if ha["correspondences"]:
                L.append("Correspondences in candidate pairs:")
                L.append("")
                L.append("| reference | Hattic | position | slots | "
                         "independent | regular |")
                L.append("|---|---|---|---|---|---|")
                for c in ha["correspondences"]:
                    L.append(f"| {c['ref']} | {c['hattic']} | "
                             f"{c['position']} | {c['support_slots']} | "
                             f"{c['independent']} | "
                             f"{'yes' if c['regular'] else 'no'} |")
            else:
                L.append("No candidate pairs, so no correspondence sets and "
                         "no correspondence recurs at all (N ≥ 3 needed).")
        m = arm["runs"]["main"]["morphology"]
        mm = m[K]
        L.append("")
        L.append(f"## Morphology (§5, A4.1): {mm['testable']} of 8 items "
                 f"testable; {mm['nontrivial']} non-trivial matches")
        L.append("")
        L.append("| item | testable | Hattic | PAA | position | consonants "
                 "| match |")
        L.append("|---|---|---|---|---|---|---|")
        for row in mm["items"]:
            if not row["comparisons"]:
                L.append(f"| {row['item']} {row['name']} | no | | | | | |")
            for c in row["comparisons"]:
                if c["position_agrees"]:
                    pos = "agree"
                elif c["ref_position"] == UNSTATED:
                    pos = ("PAA position not stated by the source; "
                           "agreement cannot be shown, not counted")
                else:
                    pos = (f"differ ({c['hattic_position']} vs "
                           f"{c['ref_position']}), not counted")
                cons = "agree" if c["consonants_agree"] else "differ"
                if c["consonants_agree"]:
                    cons += f" ({c['matching_consonants']})"
                if c.get("guttural_unaligned"):
                    cons += f"; {c['guttural_unaligned']}~∅ unscored"
                L.append(f"| {row['item']} {row['name']} | "
                         f"{'yes' if row['testable'] else 'no'} | "
                         f"{c['hattic']} | {c['ref']} | {pos} | {cons} | "
                         f"{'yes' if c['match'] else 'no'} |")
        L.append("")
        L.append(f"Hattic–Proto-Uralic (Control B, the same as in the PS "
                 f"arm): {m['hattic_uralic']['testable']} items testable, "
                 f"{m['hattic_uralic']['nontrivial']} non-trivial matches. "
                 f"Morphology strand: "
                 f"{'testable' if m['testable'] else 'not testable'} "
                 f"(needs ≥ {MORPH_MIN_TESTABLE} testable items); "
                 f"{'passes' if m['pass'] else 'does not pass'}.")
        sens = arm["sensitivity"]
        L.append("")
        L.append("## Symbols the class tables do not list")
        L.append("")
        L.append("Read as: " + "; ".join(
            f"{side} {s} → {c}" for side, d in INFERRED.items()
            if side in ("hattic", "paa", "pu")
            for s, c in d.items()) + ".")
        L.append("")
        L.append(f"Each was re-run under every class and under \"matches "
                 f"nothing\"; geminates were also read as single, and PAA "
                 f"affixes kept ({sens['runs']} re-runs, on the exploratory "
                 f"set). " + (
                     "R, R_PU and the outcome category are unchanged in "
                     "every re-run." if not any(
                         k in c for c in sens["changed"]
                         for k in ("R", "R_PU", "outcome"))
                     else "**R, R_PU or the outcome changes in at least one "
                          "re-run; see below.**"))
        if sens["changed"]:
            L.append("")
            L.append("Re-runs in which a candidate decision differs:")
            L.append("")
            for c in sens["changed"]:
                extra = {k: v for k, v in c.items() if k != "variant"}
                L.append(f"- {c['variant']}: {extra}")
    L.append("")
    return "\n".join(L)


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    if validate_data.main([argv[0], str(root)]) != 0:
        print("data do not validate; not running the comparison")
        return 1
    data = root / "data"
    hattic = read_tsv(data / "hattic.tsv")
    ps = read_tsv(data / "proto_semitic.tsv")
    pu = read_tsv(data / "control_proto_uralic.tsv")
    meanings = validate_data.prereg_meanings(root)

    runs = {
        "main": evaluate(hattic_selected(hattic, "counts"), ps, pu),
        "collated": evaluate(hattic_selected(hattic, "collated"), ps, pu),
        "exact": evaluate(hattic_selected(hattic, "counts"), ps, pu,
                          exact_only=True),
        "exploratory": evaluate(hattic_selected(hattic, "exploratory"),
                                ps, pu),
        "strict": evaluate(hattic_selected(hattic, "strict"), ps, pu),
    }
    filled = [r for r in hattic.values() if r["form"]]
    uncollated = [r for r in filled if r["provenance"] == "uncollated"]
    results = {
        "runs": runs,
        "hattic_filled": len(filled),
        "hattic_uncollated": len(uncollated),
        "sensitivity": inferred_symbol_sensitivity(
            hattic_selected(hattic, "exploratory"), ps, pu),
    }
    (root / "analysis" / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    (root / "analysis" / "results.md").write_text(render(results, meanings),
                                                  encoding="utf-8")
    paa = {"ps_outcome": runs["main"]["outcome"]}
    for src, fname, morph_kind, _ in PAA_SOURCES:
        paa[src] = paa_arm(hattic, read_tsv(data / fname), pu, morph_kind)
    reading, why = combined_reading(paa["primary"]["runs"]["main"]["outcome"],
                                    runs["main"]["outcome"])
    paa["combined"] = {"reading": reading, "reason": why}
    (root / "analysis" / "results_paa.json").write_text(
        json.dumps(paa, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    (root / "analysis" / "results_paa.md").write_text(
        render_paa(paa, meanings), encoding="utf-8")
    m = runs["main"]
    print(f"n={m['hattic_semitic']['n']} R={m['hattic_semitic']['R']} "
          f"p={m['control_A']['p']} n_PU={m['hattic_uralic']['n']} "
          f"R_PU={m['hattic_uralic']['R']} outcome: {m['outcome']}")
    for src, *_ in PAA_SOURCES:
        a = paa[src]["runs"]["main"]
        print(f"PAA {src}: n={a['hattic_afroasiatic']['n']} "
              f"R={a['hattic_afroasiatic']['R']} p={a['control_A']['p']} "
              f"outcome: {a['outcome']}")
    print(f"combined (A4.5): {reading}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

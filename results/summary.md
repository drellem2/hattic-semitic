# Result summary

**Hypothesis:** Hattic is a sister language of Proto-Semitic.
**Procedure:** [`docs/preregistration.md`](../docs/preregistration.md), with
amendments A1–A3, applied mechanically by
[`analysis/compare.py`](../analysis/compare.py). The full output, including
every compared slot and alignment, is in
[`analysis/results.md`](../analysis/results.md) and
[`analysis/results.json`](../analysis/results.json).

## Outcome category: **the data cannot decide**

The category follows from §6 before any form is compared. Only **n = 9** of
the 96 lexical slots have both a qualifying Hattic form (cited and securely
glossed, §1.2) and a Proto-Semitic form, and §6 needs n ≥ 30. That was stated
in the README when the data were assembled, before the comparison was run. The
comparison was run anyway, because §6.2 lists what is reported whatever the
outcome.

Under the strict reading of §1.1, where only forms from Soysal 2004 count,
**n = 0**. Soysal 2004 could not be viewed (A3). The A3 figures below are
reported next to that figure, not in place of it.

This result is not "no support". It says nothing for or against the
hypothesis. No resemblance among the nine compared pairs is offered as
suggestive, and none would be at this n.

### Amendment A4: the Proto-Afroasiatic arm

A4 was committed while this comparison was being prepared. It adds a second
arm, Hattic vs Proto-Afroasiatic, and says that only that arm can give support
to the sister reading. A4 leaves the Proto-Semitic arm unchanged. The result
above is therefore the registered result of the Hattic–Proto-Semitic
comparison, reported first, as A4 requires.

**The PAA arm has not been run.** No PAA form has been collected. Its n cannot
exceed the 17 qualifying Hattic slots, which is below 30 (A4.6), so it will
land in "cannot decide" whatever the PAA forms are. Under A4.5, a PAA arm that
cannot decide and a PS arm that cannot decide combine to **the data cannot
decide**. The combined reading is the same as the PS-arm result.

## Hattic–Proto-Semitic vs the controls

Main run: amendment A3, with cited and securely glossed Hattic forms only.

| | Hattic–Proto-Semitic | Control A: meaning-shuffled | Control B: Hattic–Proto-Uralic |
|---|---|---|---|
| slots compared | n = 9 | 9 (forms permuted) | n_PU = 13 |
| monoconsonantal Hattic stems (never scorable, §3.3) | 5 of 9 | — | 5 of 13 |
| candidate pairs (§3.3) | 0 | — | 0 |
| correspondences recurring ≥ 3 times | 0 | — | 0 |
| regular cognate sets | R = 0 | R_shuffle = 0 in all 1000 derangements | R_PU = 0 |
| rate | r = 0.000 | — | r_PU = 0.000 |
| p (§4.1, seed 20261003) | — | p = (1 + 1000) / 1001 = **1.000** | — |

The lexical criterion (§4.3) is not met. R = 0 < 5. Because n_PU = 13 < 20,
Control B is uninformative and condition 3 becomes p ≤ 0.01, and p = 1.000.
The lexical strand would therefore fail, but §6 uses that only when n ≥ 30,
so it does not change the category.

Sensitivity runs, all with the same procedure:

| run | n | R | n_PU | R_PU | p | category |
|---|---|---|---|---|---|---|
| main (A3, cited + secure) | 9 | 0 | 13 | 0 | 1.000 | cannot decide |
| **collated-only** (uncollated forms excluded) | 9 | 0 | 13 | 0 | 1.000 | cannot decide |
| `exact` pairs only (§2) | 7 | 0 | 10 | 0 | 1.000 | cannot decide |
| strict §1.1 (Soysal 2004 only) | 0 | 0 | 0 | 0 | — | cannot decide |
| exploratory: doubtful glosses included, outside the decision | 12 | 0 | 16 | 0 | 1.000 | — |

### Uncollated forms

**0 of the 24 Hattic forms are `uncollated`** (0%). The same holds for
Proto-Semitic (0 of 37) and Proto-Uralic (0 of 61). The collated-only run is
therefore identical to the main run. None of the result rests on uncollated
forms, and in any case there is no support for anything to rest on.

## The §6.2 items

- **n, R, r, p, R_PU, r_PU, n_PU:** in the table above.
- **Shuffle distribution:** R_shuffle = 0 in all 1000 derangements.
- **Candidate list:** empty, in every run. Of the nine Hattic–Proto-Semitic
  slots:
  - 5 have a Hattic stem with only one consonant, so §3.3 lists them and
    never scores them: 3 *to go* nu, 26 *house* vae, 51 *child* in,
    53 *to give* i̯a, 75 *to eat* tu.
  - 4 have two or more consonants and fail §3.3: 57 *good* malḫib ~ ṭyb,
    63 *soil* štarrazil ~ ʾrṣ́, 82 *to fall* zik ~ hwy, 89 *to see* kun ~ x̣zy.
    Each has a mismatch in its first or second aligned position.

  The alignments are in [`analysis/results.md`](../analysis/results.md).
- **Removed items (§3.4, loans, onomatopoeia):** none. There were no
  candidates to remove, and the data carry no loan or onomatopoeia flags.
- **Regular correspondences:** none. With no candidate pair, no
  correspondence is observed at all.
- **`exact`-only:** n = 7, R = 0, as in the table.
- **Morphology:**

  | item | Hattic | Proto-Semitic | Proto-Uralic |
  |---|---|---|---|
  | 1 1sg | doubtful (not testable) | *-ī/-ya suffix | mȣ̈ independent |
  | 2 2sg | ú-un independent; ú-/u- prefix | — | *tun independent |
  | 3 3sg | li-e-, te-, le- prefix; -e/-i̯a suffix | — | — |
  | 4 1pl | ai-/(n)i- prefix | *-na/-ni/-nu suffix | mȣ̈ independent |
  | 5 negation | taš- prefix | — | — |
  | 6 prohibitive | taš-te- prefix | — | — |
  | 7 nominal plural | u̯aₐ-, eš- prefix | — | — |
  | 8 causative | — | — | — |

  - **Hattic–Proto-Semitic:** 1 of 8 items is testable (item 4), and §5.3
    needs 4, so the morphology strand is **not testable**. In item 4 the
    consonant *n* agrees, but Hattic has a prefix and Proto-Semitic a suffix.
    Under §5.2 that is a position mismatch: it is reported here and not
    counted. Even in the same position, a single consonant would be a trivial
    match. Non-trivial matches: 0.
  - **Hattic–Proto-Uralic:** 2 items are testable. In item 2, ú-un and *tun
    are both independent words, but their consonants do not agree (n ~ t).
    In item 4, the Hattic prefix and the Proto-Uralic independent word differ
    in position. Non-trivial matches: 0.
- **Uncollated fraction and exploratory results:** 0% uncollated. The
  exploratory run, which adds the doubtful glosses, is in the table above.
  It gives n = 12 and R = 0.

## Deviations from the registration

**None.** No threshold, list, latitude or class was changed after the data
were seen. The A3 source substitutions were committed before any data.

The registration leaves some details to the implementation. These readings
were fixed in `analysis/compare.py` before its first run. They are listed
because they are choices.

- **Symbols missing from the class tables.** The tables of §3.2 and §4.2 do
  not list six symbols that occur in the data. They are read as:
  - Proto-Semitic: *x̣*, a letter of the AHD alphabet (in roots for *to
    carry*, *to see* and *sweet*), as H; *ṣ́* as S.
  - Proto-Uralic: *c* as S, *d* as T, and *γ* as H.
  - Hattic: plain *h* in one exploratory stem as H.

  Each symbol was re-run under every class and under "matches nothing", and
  Proto-Uralic geminates were also read as single: 61 re-runs in all. **R,
  R_PU and the category are the same in every re-run.** In one re-run a
  candidate appears: Proto-Uralic *d* read as M (a labial nasal, which is not
  a phonetically possible reading of *d*) makes slot 13, Hattic *tumil* vs
  Proto-Uralic *\*śådå-*, a Control B candidate. One candidate cannot make a
  regular correspondence, which needs 3.
- **Several forms in one cell.** Where a cell has `a/b` alternatives or
  several forms, the first is compared. A slash inside a Proto-Uralic form
  marks a vowel alternation and does not affect the consonants.
- **Correspondences** are counted over every scored aligned position of a
  candidate pair, matched or not (§3.5). Several of these readings are moot
  here, because there are no candidates.
- **Morphology:** a form's consonants are aligned left to right, as in §3.3.
  Hattic ai-/(n)i- is credited with its optional *n*. That reading favours a
  match, and the item still does not match because of position.

## What limits this result

The binding constraint is the Hattic data, and behind it the sources that
could be opened.

- **Opened and used:** Schuster 1974 (*Die hattisch-hethitischen
  Bilinguen* I, Teil 1) and Kammenhuber 1969 ("Hattisch", HdO), both as
  Internet Archive scans. Every Hattic form comes from them.
- **Not opened:**
  - Soysal 2004 (*Hattischer Wortschatz*), the governing source under §7.2:
    the only online copy is lending-restricted.
  - Klinger 1996 (StBoT 37): no open copy was found.
  - On the Semitic side, Kogan 2011, the SED and Huehnergard 2019.

**How many more slots Soysal 2004 would fill cannot be estimated from what
was viewed.** Its word list and index were never seen, and nothing in
Schuster 1974 or Kammenhuber 1969 gives a count to extrapolate from. No
figure is offered.

What can be said from the data as assembled is a ceiling. The Proto-Semitic
side fills only 37 slots from the one viewable source, so **n can be at most
37** however many Hattic slots a re-collation fills. To reach n ≥ 30, Hattic
would need a cited, securely glossed form in at least 30 of those 37 slots.
It has one in 9 now, so it would need 21 of the remaining 28: *water, mouth,
blood, name, wing, arm/hand, fly, ear, bitter, to say, tooth, to hit, fish,
to stand, new, to burn, to know, to laugh, to hear, to carry, eye, tail,
sweet, shade, salt, small, in, to crush*. A real test therefore needs a
re-collation on both sides: Soysal 2004 for Hattic, and Kogan 2011 or the SED
for Proto-Semitic. Control B also stays uninformative until n_PU ≥ 20; it is
13 now.

Any such re-collation must be recorded as a new dated amendment, made before
the comparison is re-run (see [`data/README.md`](../data/README.md)). After
that, `python3 analysis/compare.py` reproduces every number here.

## Reproduce

```
python3 analysis/compare.py      # validates data/, writes analysis/results.{md,json}
python3 -m unittest analysis/test_compare.py analysis/test_validate_data.py
```

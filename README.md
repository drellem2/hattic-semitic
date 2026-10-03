# hattic-semitic

Testing the hypothesis that **Hattic is a sister language of Proto-Semitic**,
using the traditional comparative method.

## Result

**The data cannot decide.** Only 17 Hattic basic-vocabulary words could be
sourced, with a secure gloss, from editions that are openly viewable. The
standard Hattic lexicon, Soysal 2004, could not be opened. The test was
fixed in advance to need at least 30 compared words. Hattic was compared
with Proto-Semitic (9 slots, from Huehnergard's *American Heritage
Dictionary* appendix of Semitic roots) and with Proto-Afroasiatic (17
slots, from the Militarev–Stolbova database, with Orel & Stolbova 1995 as a
check). Proto-Afroasiatic reconstructions are themselves contested. Both
comparisons fall short of 30, so the outcome follows from the counts alone,
and the combined reading is "cannot decide". As description only, not as
evidence: no comparison, and no control, produced a single candidate
cognate. At these numbers the pre-registration does not let that count
against the hypothesis. Access to Soysal 2004 or Klinger 1996, or newly
glossed Hattic vocabulary, could change the answer, and the pipeline is
ready to re-run. The full write-up is in
[`docs/findings.md`](docs/findings.md).

## Hypothesis

Hattic — the non-Indo-European language of central Anatolia known from
cuneiform texts of the second millennium BCE, chiefly from the Hittite
archives — descends from a common ancestor shared with Proto-Semitic.
In other words, Hattic and Proto-Semitic are coordinate branches of a
single family, not related by borrowing alone.

## Prior

This hypothesis is not the mainstream view, and the repository starts from
that position honestly:

- Hattic is conventionally treated as a **language isolate**. Proposed
  external links are mainly to the Northwest Caucasian languages; no link to
  Semitic has mainstream support.
- The **securely glossed Hattic vocabulary is small**. Much of the corpus is
  ritual and bilingual (Hattic–Hittite) text, and many words have uncertain or
  context-only meanings.
- The **morphological profiles differ**: Hattic is heavily prefixing, while
  Semitic morphology is organised around consonantal roots and vowel patterns.
  Any shared morphology must be argued against that background, not assumed.

## Method

The traditional comparative method — not a statistical or computational
similarity pipeline:

1. **Regular, recurrent sound correspondences** across basic vocabulary.
   A correspondence counts only if it recurs across multiple independent
   comparanda; isolated look-alikes do not count.
2. **Shared non-trivial morphology**: pronouns, verbal and nominal affixes,
   and other grammatical material that is unlikely to be borrowed or to
   resemble by chance.
3. **Controls for chance and contact**: onomatopoeia, nursery words, and
   likely loans (including through Akkadian, Hittite, and other contact
   languages of Anatolia and Mesopotamia) are identified and set aside.

## Outcomes

Results will be reported **whichever way they fall**. Three outcomes are
live and each is reportable:

- **Supported** — regular correspondences and shared morphology beyond what
  chance and contact explain.
- **Not supported** — the comparanda fail the criteria above.
- **The data cannot decide** — the securely glossed Hattic material is too
  small or too uncertain to test the hypothesis either way.

## Data provenance

Provenance is the main risk to this project. Every form carries a provenance
field.

- **`cited`** gives the work, the page or entry, and the URL where the source
  text was viewed during collection.
- **`uncollated`** marks a form that was not checked against a viewed source.

A form known only from memory counts as uncollated, even if the book and page
it should be in can be named. None of the current data is uncollated.
Forms are never invented to fill an empty slot. See [`data/`](data/).

## Layout

- [`data/`](data/) — lexical and morphological comparanda, with provenance
- [`analysis/`](analysis/) — correspondence sets and comparisons
- [`docs/`](docs/) — pre-registration and method notes
- [`results/`](results/) — the result summary

## Status

1. **Pre-registered.** The comparison list, matching rules, chance-baseline
   controls and outcome criteria are fixed in
   [`docs/preregistration.md`](docs/preregistration.md), which was committed
   before any data. Amendments A1–A3 in its §9 were also committed before any
   data. They check the word list, define `cited` as "viewed during
   collection", and record which sources could not be viewed and what
   replaced them.
   Amendment A4, committed before any Proto-Afroasiatic form was collected,
   adds a second arm comparing Hattic with Proto-Afroasiatic, the node a
   sister of Semitic would share with it; only that arm can give support to
   the sister reading. Amendment A5 records that the first source in A4's
   order, the Militarev–Stolbova Afroasiatic database (Tower of Babel), could
   be viewed, which makes it the primary PAA source. A5 also fixes how A4's
   slot rules are read for that database. It was committed before any PAA
   slot was filled.
   Amendment A6, committed before any slot was filled from it, restates
   those rules for Orel & Stolbova 1995, the next PAA source. A4 requires the
   PAA arm also to be run on that source alone, as a sensitivity check that
   is never decisive. A7 records two clerical points found while filling it.
2. **Data assembled.** See [`data/`](data/) and its README for the full
   counts and the source list.

| | lexical slots filled (of 96) | cited (viewed) | uncollated |
|---|---|---|---|
| Hattic | 24, of which **17 securely glossed** and counting toward the decision | 24 | 0 (0%) |
| Proto-Semitic | 37 | 37 | 0 (0%) |
| Proto-Afroasiatic (second arm) | 80 | 80 | 0 (0%) |
| Proto-Afroasiatic, sensitivity list (Orel & Stolbova 1995) | 75 | 75 | 0 (0%) |
| Proto-Uralic (control) | 61 | 61 | 0 (0%) |

**What could not be sourced.**

- The governing Hattic dictionary, Soysal 2004, could not be viewed, because
  the only online copy is lending-restricted. Every Hattic form instead comes
  from Schuster 1974 and Kammenhuber 1969, both viewed as scans. Read
  strictly, the original registration therefore has **0** qualifying Hattic
  slots.
- The two higher-precedence Proto-Semitic sources (Kogan 2011, the SED) and
  the registered Proto-Semitic grammar (Huehnergard 2019) could not be viewed
  either.

Only 9 lexical slots are filled with a qualifying Hattic form and a
Proto-Semitic form, and 17 with a qualifying Hattic form and a
Proto-Afroasiatic form, against the n ≥ 30 that §6 and A4.2 require. The
PAA count is capped by the Hattic side: all 17 qualifying Hattic slots have
a PAA form. Only 1 of the 8 morphology items is testable for
Proto-Semitic, and 3 for Proto-Afroasiatic.

3. **Comparison run.** The outcome is **the data cannot decide**: n = 9,
   and §6 needs n ≥ 30. The category follows from n alone. The full procedure
   was still run and found:
   - no candidate pairs, so R = 0;
   - Control A shuffle p = 1.000;
   - Control B: n_PU = 13, R_PU = 0;
   - morphology: 1 of 8 items testable, 0 non-trivial matches.

   The collated-only result is the same, because no form is uncollated. This
   is the Proto-Semitic arm.
4. **Proto-Afroasiatic arm run (A4).** Its outcome is also **the data cannot
   decide**: n = 17 < 30, as A4.6 fixed before any PAA data. The full
   procedure found no candidate pairs, so R = 0, with Control A p = 1.000,
   and 3 of 8 morphology items testable with 0 non-trivial matches. The
   A4.1 sensitivity run on Orel & Stolbova 1995 agrees (n = 16, R = 0). The
   combined A4.5 reading is **the data cannot decide**. See
   [`results/summary.md`](results/summary.md).

## Licence

- **Text and data** — this README, [`docs/`](docs/) and [`data/`](data/) —
  are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/);
  see [`LICENSE-DATA`](LICENSE-DATA).
- **Code** — [`analysis/`](analysis/) and any scripts — is licensed under the
  MIT License; see [`LICENSE`](LICENSE).

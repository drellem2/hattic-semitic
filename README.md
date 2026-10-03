# hattic-semitic

Testing the hypothesis that **Hattic is a sister language of Proto-Semitic**,
using the traditional comparative method.

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
- [`docs/`](docs/) — method notes, source notes, and results

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
   the sister reading.
2. **Data assembled; no comparison run yet.** See [`data/`](data/) and its
   README for the full counts and the source list.

| | lexical slots filled (of 96) | cited (viewed) | uncollated |
|---|---|---|---|
| Hattic | 24, of which **17 securely glossed** and counting toward the decision | 24 | 0 (0%) |
| Proto-Semitic | 37 | 37 | 0 (0%) |
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
Proto-Semitic form, against the n ≥ 30 that §6 requires. Only 1 of the 8
morphology items is testable. As assembled, the data point to the
pre-registered outcome **"the data cannot decide"**. That is stated here
before any comparison has been run.

## Licence

- **Text and data** — this README, [`docs/`](docs/) and [`data/`](data/) —
  are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/);
  see [`LICENSE-DATA`](LICENSE-DATA).
- **Code** — [`analysis/`](analysis/) and any scripts — is licensed under the
  MIT License; see [`LICENSE`](LICENSE).

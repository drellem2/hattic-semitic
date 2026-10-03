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

Provenance is the main risk to this project. Every Hattic and Semitic form
carries a provenance field: `cited` (with the work and page or entry where
known) or `uncollated` (not yet checked against a published source). The
results will state plainly what fraction of the data used is uncollated.
Forms are never invented to fill an empty slot. See [`data/`](data/).

## Layout

- [`data/`](data/) — lexical and morphological comparanda, with provenance
- [`analysis/`](analysis/) — correspondence sets and comparisons
- [`docs/`](docs/) — method notes, source notes, and results

## Status

Just started. No data or results yet.

## Licence

- **Text and data** — this README, [`docs/`](docs/) and [`data/`](data/) —
  are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/);
  see [`LICENSE-DATA`](LICENSE-DATA).
- **Code** — [`analysis/`](analysis/) and any scripts — is licensed under the
  MIT License; see [`LICENSE`](LICENSE).

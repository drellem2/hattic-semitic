# Findings: is Hattic a sister language of Proto-Semitic?

**Result: the data cannot decide.**

Only 17 Hattic basic-vocabulary words could be taken from editions that are
openly viewable with a gloss their editors give without doubt. The test was
fixed in advance to need at least 30 compared words, so it could not reach a
verdict either way. The standard Hattic dictionary, Soysal 2004, could not be
opened. Without it, or new Hattic material, the question stays open.

This is not a negative result. It is neither evidence for the hypothesis nor
evidence against it.

---

## 1. The hypothesis

Hattic was spoken in central Anatolia before the Hittites. It is known from
cuneiform texts of the second millennium BCE, mostly ritual texts copied in
the Hittite archives, some of them with a Hittite translation alongside.

The hypothesis tested here is that **Hattic and Proto-Semitic are sister
languages**. On this view they descend from a common ancestor, and their
resemblances are not due to borrowing alone.

If Hattic were a sister of Semitic, the ancestor the two share would be
**Proto-Afroasiatic**, the ancestor of Semitic, Egyptian, Berber, Chadic,
Cushitic and Omotic. So the study compares Hattic with two reconstructed
languages:

- **Proto-Semitic**, the ancestor of the Semitic languages; and
- **Proto-Afroasiatic**, the node a sister of Semitic would share with it.

Only the Proto-Afroasiatic comparison can support the *sister* reading. A
language that resembles Proto-Semitic alone could equally have borrowed from
a Semitic language, and Hattic was in long contact with Akkadian speakers.

## 2. The prior

The hypothesis starts well outside the mainstream, and the study said so
before it began.

- **Hattic is usually treated as a language isolate.** The external links
  that have been proposed are mainly to the Northwest Caucasian languages. No
  link to Semitic has mainstream support.
- **Its securely glossed vocabulary is small.** Many Hattic words are known
  only from context, or have meanings the editors mark as uncertain.
- **The grammars are built differently.** Hattic builds words mainly with
  prefixes. Semitic builds them from consonantal roots and vowel patterns,
  with suffixes and some prefixes. Any shared grammar has to be shown against
  that background.

"The data cannot decide" was named in advance as a likely outcome.

## 3. Method

The study uses the **traditional comparative method** of historical
linguistics, not a statistical similarity score. Relationship is claimed only
on two kinds of evidence:

1. **Regular sound correspondences** across basic vocabulary. A pairing of
   sounds (Hattic *t* for Semitic *\*t*, say) counts as regular only if it
   recurs in at least three independent word pairs. One-off look-alikes do
   not count.
2. **Shared grammar that is unlikely to be chance**: pronouns, negation,
   plural and causative markers, agreeing in function, in position (prefix,
   suffix or separate word) and in more than a single consonant.

### Fixed in advance

Every rule was written down and committed **before any data were
collected**, in [`preregistration.md`](preregistration.md) (commit
[`5112743`](https://github.com/drellem2/hattic-semitic/commit/51127434523a9702a5cb0d0d3ff3e753ab490d73)).
The repository's history shows that this commit comes before every data and
results commit. The registration fixes:

- **the word list**: the 100 meanings of the Leipzig–Jakarta list, which was
  built from the meanings languages least often borrow. Four grammatical
  items (*I*, *you*, *he/she*, *not*) go to the grammar comparison, which
  leaves 96 word slots;
- **one form per slot and per language**, chosen by rule from named sources,
  with no form guessed or supplied from memory;
- **narrow meaning matches**: the two words must mean the same thing, with
  only five named exceptions such as *soil* ~ *earth* and *wood* ~ *tree*;
- **sound classes and matching rules**, under which a word pair becomes a
  candidate cognate only if at least two consonants match and the first two
  do not clash;
- **two chance controls**:
  - **Control A** shuffles the Hattic words among the meanings 1000 times and
    asks how often the same procedure finds as much by chance;
  - **Control B** runs the same procedure against Proto-Uralic, a
    well-reconstructed family nobody has linked to Hattic;
- **the decision rule**:

  | outcome | condition |
  |---|---|
  | the data cannot decide | fewer than 30 word slots can be compared |
  | no support | at least 30 slots, and the regular correspondences do not beat the controls |
  | support | at least 30 slots, the correspondences beat both controls, **and** shared grammar passes too |

  Thirty is the floor because with fewer slots a sound pairing can barely
  recur three times even between related languages, and the shuffle control
  is too coarse to read.

### Amendments

Seven dated amendments (A1–A7, in §9 of the registration) were added as the
study went on. Each one states what had and had not been seen when it was
written. None changed a threshold after a comparison was run.

- **A1–A3**
  ([`abc042e`](https://github.com/drellem2/hattic-semitic/commit/abc042ea4815d21a19d926d2f2f7ba1ecb0991a2)),
  before any data. They confirm the word list, define a form as *cited* only
  if its source was actually viewed during collection, and name substitutes
  for the sources that could not be opened (section 4 below).
- **A4**
  ([`79dcccb`](https://github.com/drellem2/hattic-semitic/commit/79dcccb03f872d7b1b8dd4d6fe92a56c27525701)),
  before any Proto-Afroasiatic source was opened. It adds the
  Proto-Afroasiatic comparison, with the same threshold of 30 and the same
  controls, and says how the two comparisons combine. A4 was written after
  the Hattic and Proto-Semitic word lists were committed, but before the
  Proto-Semitic comparison was run. It already predicted, from the Hattic
  count alone, that both comparisons would end in "cannot decide".
- **A5–A7**
  ([`be4240c`](https://github.com/drellem2/hattic-semitic/commit/be4240cfdaa23c9c2b3530e84930f9b705c368c6),
  [`19d02df`](https://github.com/drellem2/hattic-semitic/commit/19d02df2cc6fe4e26cfa6f5234ead134885ca01e),
  [`3f8c416`](https://github.com/drellem2/hattic-semitic/commit/3f8c416133bcc20b3625231c15f1d41fe7080ad7)),
  each committed before any slot was filled from the source it covers. They
  fix which Proto-Afroasiatic sources were used and how their entries are
  read.

Once the data were frozen, the comparison was run mechanically by
[`analysis/compare.py`](../analysis/compare.py), and the same procedure was
used for every control.

## 4. Data, and the limits of its provenance

Every form in [`data/`](../data/) records where it came from. It is either
`cited`, with the work, the page or entry, and the URL where it was viewed,
or `uncollated`. **None of the forms is uncollated** (0%). Nothing was
entered from memory, and no form was invented to fill a gap. A slot that no
viewed source fills is left empty.

The weakness is not in the forms that were collected. It is in **which
sources could be opened**.

### Hattic

- **Soysal 2004**, *Hattischer Wortschatz*, is the standard Hattic lexicon
  and the governing source under the registration. It **could not be
  opened**: the only online copy is lending-restricted.
- **Klinger 1996** (StBoT 37), the registered source for Hattic grammar,
  could not be found in any open copy either.
- Every Hattic form therefore comes from two older works, viewed as scans:
  Schuster 1974, an edition of the Hattic–Hittite bilingual texts, and
  Kammenhuber 1969, a grammatical sketch. Both predate Soysal 2004, and some
  of their glosses may since have been revised.

These two works fill **24** of the 96 slots. Of those, **17** have a gloss
the source gives without a doubt marker, and only those 17 count toward the
decision. Read strictly, the registration counts only forms from Soysal
2004, so the strict count is **0**. The results below follow amendment A3,
which allows the substitutes, and are reported next to that strict figure,
not in place of it.

### Proto-Semitic

The two preferred sources, Kogan 2011 and the *Semitic Etymological
Dictionary*, could not be viewed. Neither could the registered grammar,
Huehnergard 2019. The Proto-Semitic forms come from the third source in the
registered order, **John Huehnergard's appendix of Semitic roots in the
*American Heritage Dictionary*** (5th ed., 2011). It lists only roots with
English descendants, so it fills just 37 of the 96 slots, and it gives
almost no grammar.

### Proto-Afroasiatic

**Proto-Afroasiatic reconstructions are contested.** The available
reconstructions disagree about the consonant inventory, about how sounds
correspond between the branches, and about many individual roots, and each
of them has been sharply criticised. The registration therefore fixes one
source per run and never mixes sources slot by slot.

- **Primary source: the Militarev–Stolbova Afroasiatic etymological
  database** (Tower of Babel project, online). It was chosen first in
  advance, because it is the most recent, it lists reflexes branch by
  branch, and its Semitic side comes from the same school as the preferred
  Proto-Semitic sources. It fills 80 slots.
- **Sensitivity source: Orel & Stolbova 1995**, *Hamito-Semitic Etymological
  Dictionary*. The whole comparison was run on it alone as a check, which
  the registration says can never change the outcome. It fills 75 slots.
- A form counts only if the source assigns it to Proto-Afroasiatic itself,
  with reflexes in at least two branches, one of them not Semitic.

### Control

Proto-Uralic forms come from Sammallahti 1988 and the *Uralisches
etymologisches Wörterbuch* (via the Uralonet database). They fill 61 slots.

The full source list, the counts and what each source could not supply are
in [`data/README.md`](../data/README.md).

## 5. Result

### The pre-registered category: the data cannot decide

| | Hattic vs Proto-Semitic | Hattic vs Proto-Afroasiatic (primary) | Proto-Afroasiatic, sensitivity run |
|---|---|---|---|
| word slots compared (30 needed) | **9** | **17** | 16 |
| candidate cognate pairs | 0 | 0 | 0 |
| regular correspondences | 0 | 0 | 0 |
| regular cognate sets | 0 | 0 | 0 |
| Control A: shuffle p (1000 shuffles) | 1.000 | 1.000 | 1.000 |
| Control B: Hattic vs Proto-Uralic, slots compared and cognate sets | 13 and 0 | 13 and 0 | 13 and 0 |
| grammar items testable (4 of 8 needed) | 1 | 3 | 0 |
| non-trivial grammar matches | 0 | 0 | 0 |
| **outcome** | **cannot decide** | **cannot decide** | cannot decide |

The category follows from the number of compared slots alone. With 9 and 17
slots against a floor of 30, it was fixed before any word was compared. A4
had predicted it in writing before any Proto-Afroasiatic data existed.

**Combined reading.** A4 says only the Proto-Afroasiatic comparison can
support the sister reading, and that if it cannot decide, the Proto-Semitic
comparison's result decides only when it is "no support". Both comparisons
cannot decide, so the combined result is **the data cannot decide**.

### What was observed, as description only

The full procedure was run anyway, because the registration requires every
figure to be reported whatever the outcome. **In every comparison, the
compared slots produced no candidate cognate at all**, so there are no sound
correspondences to report.

- Of the 9 Hattic–Proto-Semitic slots, 5 have a Hattic stem of one consonant
  (*nu* "go", *vae* "house", *in* "child", *i̯a* "give", *tu* "eat"). The
  rules never score one-consonant stems, because a single matching consonant
  is too likely by chance.
- The other 4 Proto-Semitic slots, and the multi-consonant
  Proto-Afroasiatic slots, clash in their first two consonants, or match in
  only one.
- The Uralic control also found nothing (0 cognate sets in 13 slots).
- In the shuffle control, all 1000 shuffles also found nothing.

**This does not count against the hypothesis.** The registration does not
allow it to: below 30 slots, the absence of regular correspondences is what
the procedure would also be likely to show for two related languages. The
control is also silent. Hattic–Proto-Uralic finds as little as
Hattic–Semitic, so nothing separates the real comparison from chance in
either direction. The Uralic control has only 13 slots, under the 20 the
registration needs for it to be informative.

The grammar comparison could not be run at all: at least 4 of the 8 items
must have a sourced form on both sides, and no comparison reached that. The
one or two consonants that do agree, such as the *n* of Hattic first person
plural *(n)i-* and Proto-Semitic *\*-na/-ni/-nu*, are single consonants, and
some of them are in the wrong position (a Hattic prefix against a Semitic
suffix). The registration counts neither.

### Checks

- **Uncollated forms:** none, so the run on collated forms only is identical
  to the main run.
- **Exact meaning matches only:** n = 7 (Proto-Semitic) and 14
  (Proto-Afroasiatic), with no cognate sets.
- **Proto-Afroasiatic forms with at least two non-Semitic branches:** n = 14
  on each source, with no cognate sets.
- **Doubtful Hattic glosses included** (exploratory, outside the decision):
  n = 12, 21 and 18, with no cognate sets.
- **Interpretive choices:** symbols the class tables did not list were re-run
  under every reading, more than 60 re-runs per comparison. None changed a
  cognate-set count or the category.

The full output, with every compared slot and alignment, is in
[`results/summary.md`](../results/summary.md),
[`analysis/results.md`](../analysis/results.md) and
[`analysis/results_paa.md`](../analysis/results_paa.md).

## 6. What would change the answer

The binding constraint is the number of securely glossed Hattic words that
could be sourced.

- **Access to Soysal 2004**, the standard Hattic lexicon, or to Klinger 1996.
  This is the most direct route. Their word lists were never seen, so how
  many slots they would fill cannot be estimated, and no figure is offered.
- **Newly glossed Hattic vocabulary**, from new bilingual texts or
  re-editions, would have the same effect.

How far each comparison is from a decision:

- **Proto-Afroasiatic.** The primary database fills 80 slots and already
  covers all 17 qualifying Hattic slots, so the limit is on the Hattic side
  alone. The comparison reaches 30 once **13 more** of those 80 slots have a
  sourced, securely glossed Hattic word.
- **Proto-Semitic.** The one viewable source fills only 37 slots, so this
  comparison can never exceed 37. Reaching 30 would need Hattic words in 21
  of the remaining 28. A real test needs Kogan 2011 or the *Semitic
  Etymological Dictionary* as well.
- **The Uralic control** becomes informative at 20 slots. It has 13.
- **Grammar** needs at least 4 of the 8 items testable. That needs a
  Proto-Semitic grammar (Huehnergard 2019) or a Proto-Afroasiatic survey
  (Hayward 2000), neither of which could be opened, as well as better Hattic
  coverage.

Even at 30 slots, "support" needs regular correspondences that beat both
controls *and* shared grammar. Even then, the comparative method shows
relatedness, not the shape of the family tree. Showing that Hattic is
specifically a *sister* of Semitic, rather than a more distant relative,
would need shared innovations, which this study does not test.

### Re-running

The pipeline is ready to re-run on new data:

- the comparison script, [`analysis/compare.py`](../analysis/compare.py);
- the data validators ([`analysis/validate_data.py`](../analysis/validate_data.py))
  and their tests;
- the frozen pre-registration with amendments A1–A7.

New sources must be recorded in a new dated amendment, made before the
comparison is re-run. After that:

```
python3 analysis/compare.py
python3 -m unittest analysis/test_compare.py analysis/test_validate_data.py
```

reproduces or updates every number here.

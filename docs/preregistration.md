# Pre-registration

**Hypothesis:** Hattic is a sister language of Proto-Semitic.
**Registered:** 2026-10-03, before any Hattic, Semitic or control form was
collected into this repository and before any comparison was made.
**Status:** frozen. Changes after this point go only in the
[Amendments](#9-amendments) section, dated, with a statement of what had or had
not been seen when the change was made.

This document fixes, in advance, what will be compared, how a match is judged,
what counts as a regular correspondence, how chance is controlled for, and what
result falls into each of the three outcome categories. Its purpose is to
remove the analyst's freedom to choose the comparison after seeing which
meanings happen to resemble each other. The `git log` of this repository is the
evidence that it came first: the commit adding this file precedes every commit
that adds data under `data/` or results under `analysis/`.

Bibliographic details of the works named below are given as the registrant
understood them at registration. They are to be checked when the sources are
collated; a correction to a page number or edition is a clerical amendment,
not a change of source.

---

## 1. Comparison list

**The comparison list is the Leipzig–Jakarta list of basic vocabulary**
(Tadmor, Haspelmath & Taylor 2010, "Borrowability and the notion of basic
vocabulary", *Diachronica* 27(2): 226–246; derived from the Loanwords in the
World's Languages project, Haspelmath & Tadmor eds. 2009). It is chosen because
it was constructed empirically from the meanings *least* often borrowed, which
matters for a language that was in long contact with Akkadian- and
Hittite-speaking communities.

No other meaning is added to the lexical comparison. The Swadesh lists are not
used, in whole or in part, so that the list cannot be enlarged after the fact.

The 100 meanings, as transcribed for convenience (the published list governs
if this transcription differs from it in any slot):

| # | meaning | # | meaning | # | meaning | # | meaning |
|---|---|---|---|---|---|---|---|
| 1 | fire | 26 | house | 51 | child (kin term) | 76 | thigh |
| 2 | nose | 27 | stone/rock | 52 | egg | 77 | thick |
| 3 | to go | 28 | bitter | 53 | to give | 78 | long |
| 4 | water | 29 | to say | 54 | new | 79 | to blow |
| 5 | mouth | 30 | tooth | 55 | to burn (intr.) | 80 | wood |
| 6 | tongue | 31 | hair | 56 | not | 81 | to run |
| 7 | blood | 32 | big | 57 | good | 82 | to fall |
| 8 | bone | 33 | one | 58 | to know | 83 | eye |
| 9 | you (2sg) | 34 | who? | 59 | knee | 84 | ash |
| 10 | root | 35 | he/she (3sg) | 60 | sand | 85 | tail |
| 11 | to come | 36 | to hit/beat | 61 | to laugh | 86 | dog |
| 12 | breast | 37 | leg/foot | 62 | to hear | 87 | to cry/weep |
| 13 | rain | 38 | horn | 63 | soil | 88 | to tie |
| 14 | I (1sg) | 39 | this | 64 | leaf | 89 | to see |
| 15 | name | 40 | fish | 65 | red | 90 | sweet |
| 16 | louse | 41 | yesterday | 66 | liver | 91 | rope |
| 17 | wing | 42 | to drink | 67 | to hide | 92 | shade/shadow |
| 18 | flesh/meat | 43 | black | 68 | skin/hide | 93 | bird |
| 19 | arm/hand | 44 | navel | 69 | to suck | 94 | salt |
| 20 | fly (insect) | 45 | to stand | 70 | to carry | 95 | small |
| 21 | night | 46 | to bite | 71 | ant | 96 | wide |
| 22 | ear | 47 | back | 72 | heavy | 97 | star |
| 23 | neck | 48 | wind | 73 | to take | 98 | in |
| 24 | far | 49 | smoke | 74 | old | 99 | hard |
| 25 | to do/make | 50 | what? | 75 | to eat | 100 | to crush/grind |

**Slots moved to the morphology strand.** Slots 9 (you), 14 (I), 35 (he/she)
and 56 (not) are grammatical items. They are compared only in the morphology
strand (§5) and are excluded from the lexical count, so that no resemblance is
counted twice. The lexical strand therefore has **96 slots**.

### 1.1 One form per slot, per language, fixed before comparison

Each slot receives at most one form from each language, chosen by rule:

- **Hattic:** the form that the primary Hattic source (§7.2) glosses with that
  meaning. If it gives more than one, the one it treats as most secure; if
  still tied, the one with the most attestations it cites; if still tied, the
  first in its alphabetical order.
- **Proto-Semitic:** the reconstruction that the highest-precedence Semitic
  reference (§7.1) gives for that meaning; if it gives more than one, the
  first-listed.
- **Controls:** the same rule, with the control's own references (§4).

A slot with no qualifying form is left **empty** and is not compared. No form
is reconstructed, guessed, or supplied from memory to fill it.

**Order of commits.** The filled Hattic slot list (with segmentation, §3.1) is
committed first; the Proto-Semitic and control slot lists after it; the
comparison after both. Slot fillers are not revised after the comparison is
run except by a dated amendment (§9).

### 1.2 Which Hattic forms count

A Hattic form fills a slot **for the purpose of the decision** only if its
provenance is `cited` — checked against a published source, with work and page
or entry — **and** that source gives the gloss without marking it as doubtful
(no "?", "unclear", "perhaps", or a gloss offered only from context).

Forms that are `uncollated`, or whose gloss is marked doubtful, may be recorded
and compared, but they are reported in a separate exploratory table and **do
not count toward any criterion in §4–§6.**

---

## 2. Semantic latitude

Narrow semantic latitude is the main guard against chance, so it is narrow.

A Hattic form and a reference form fill the same slot only if each one's
attested gloss is the slot meaning, allowing **only**:

1. the alternatives already merged in the list's own glosses (stone/rock,
   flesh/meat, arm/hand, leg/foot, skin/hide, shade/shadow, to hit/beat,
   to do/make, to cry/weep, to crush/grind); slot 51 "child" means a kin term,
   so "son" or "daughter" (offspring) fills it; and
2. this closed list of five further equivalences, and no others:
   - soil ~ earth, ground
   - wood ~ tree
   - to go ~ to walk
   - to say ~ to speak
   - to see ~ to look

Not permitted: any other semantic shift, however natural (e.g. "night" ~
"evening", "fire" ~ "to burn", "mouth" ~ "lip"); cross-part-of-speech matches
(a noun slot is filled by a noun, a verb slot by a verb or a verbal root); and
compounds or derived forms whose base has a different meaning.

Every compared pair is tagged `exact` or `permitted-shift`. Results are
reported both for all pairs and for `exact` pairs alone (sensitivity check).

---

## 3. Phonetic matching rules and regularity

### 3.1 What is compared

- **Hattic:** the **stem**, after removing affixes, as segmented by a cited
  grammatical source (§7.2). If no cited source segments the word, it is
  compared whole and tagged `unsegmented`. Segmentation is recorded in the
  Hattic data commit, before any reference form is entered.
- **Proto-Semitic:** the **root consonants**, in order, as given by the
  reference.
- **Vowels are not compared.** Hattic vowels are poorly recoverable from
  cuneiform spelling, and Semitic roots are consonantal.

Hattic consonants are read from the transliteration of the cited source.
Cuneiform conventions are neutralised identically for every comparison:
doubled writing of a consonant is read as single; the voiced/voiceless contrast
in stop signs is ignored; a consonant written with WA-series signs (variously
interpreted as /w/ or /f/) is classed as a labial (P).

### 3.2 Consonant classes

A consonant pair is a **class match** if both belong to the same class:

| class | Proto-Semitic | Hattic (as transliterated) |
|---|---|---|
| P labial obstruent | *p, *b | p, b, WA-series consonant |
| M | *m | m |
| T dental stop | *t, *d, *ṭ | t, d |
| S sibilant/affricate/interdental | *s, *z, *ṣ, *š, *ś, *ṯ, *ḏ, *ṯ̣ (*ṱ) | s, š, z |
| K velar/uvular | *k, *g, *q | k, g |
| N | *n | n |
| R liquid | *r, *l | r, l |
| W glide | *w, *y | y (where written) |
| H guttural | *ʔ, *ʕ, *h, *ḥ, *ḫ, *ġ | ḫ |

and additionally **T ~ S** counts as a class match (dental stops and sibilants
or affricates interchange frequently enough across families that excluding
them would be arbitrary). No other cross-class pairing counts.

**Gutturals.** Cuneiform cannot write most Semitic gutturals. A Proto-Semitic
guttural may therefore be aligned with **nothing** in the Hattic form. Such an
alignment is permitted (at most one per pair) but is **unscored**: it neither
counts as a match nor as a mismatch. A guttural matched to a written Hattic ḫ
is scored normally.

### 3.3 Candidate pairs

Within a slot, the Hattic stem consonants and the Proto-Semitic root
consonants are aligned left to right from the first consonant, with at most one
unscored guttural-to-nothing alignment. The pair is a **candidate** if:

- at least **two** aligned positions are scored class matches, and
- neither of the first two aligned (non-skipped) positions is a mismatch.

A Hattic stem with only one consonant can never be a candidate. Monoconsonantal
resemblances are too likely by chance to count lexically; they are listed but
not scored.

### 3.4 Loans and non-arbitrary forms

Before regularity is computed, a candidate is removed (and listed as removed,
with the reason) if:

- it is plausibly a **loan**: the Hattic form agrees with an attested Akkadian
  (or Sumerian, Hittite, Hurrian) form more closely than with the
  Proto-Semitic reconstruction, specifically by sharing a sound change or
  shape peculiar to that language; or
- it is **onomatopoeic or nursery** vocabulary (e.g. forms of the
  *mama/papa/baba* type, sound-imitative verbs of blowing, sucking or
  laughing).

### 3.5 Regular correspondences

A **correspondence** is a pairing of one Proto-Semitic phoneme with one Hattic
phoneme in a given position (root-initial, or non-initial), observed in a
scored aligned position of a candidate pair. Correspondences are counted at
the level of individual phonemes, not classes.

Two candidate pairs are **independent** unless they share the same Hattic stem
or the same Proto-Semitic root, or one is derived from the other.

A correspondence is **regular** if it recurs in **N ≥ 3 independent candidate
pairs.**

A candidate pair is a **regular cognate set** if at least two of its scored
correspondences are regular.

**Consistency.** For each Proto-Semitic phoneme, the regular correspondences
it enters must not conflict without conditioning: if one Proto-Semitic
phoneme has two or more regular Hattic reflexes in the same position, each
reflex beyond the most frequent one must have a stated phonological
conditioning environment that holds in every pair showing it. Pairs whose
only regular status rests on an unconditioned competing reflex are not counted
as regular cognate sets.

The lexical statistic is **R**, the number of regular cognate sets, and the
rate **r = R / n**, where n is the number of lexical slots compared (filled on
both sides).

### 3.6 The procedure is mechanical after the data are frozen

Every judgement in §1–§3.4 that requires a linguist (slot filling, gloss
security, segmentation, loan/onomatopoeia flags) is made **in the data**, and
committed, before any comparison is run. The comparison itself (§3.2–§3.5) is
rule-based, so that it can be run identically on Hattic–Semitic and on every
control. It is implemented as a script under `analysis/`.

---

## 4. Chance baseline and the lexical support criterion

The identical procedure (§3.2–§3.5) is run on two controls.

### 4.1 Control A — meaning-shuffled Hattic vs Proto-Semitic

The n Hattic forms of the n compared slots are permuted among those slots so
that no form stays in its own slot (a derangement), and the full procedure is
re-run, regularity included. This is repeated **1000 times** with a
pseudo-random generator seeded with **20261003**. The empirical p-value is

  p = (1 + number of shuffles with R_shuffle ≥ R_observed) / 1001.

This control keeps the phonotactics of both sides exactly as they are and
destroys only the meaning alignment, so it measures how many regular cognate
sets this procedure finds between these two particular inventories by chance.

### 4.2 Control B — Hattic vs Proto-Uralic

Proto-Uralic is a well-reconstructed proto-language for which no relationship
with Hattic has been proposed. Its 96 lexical slots are filled by the rule of
§1.1 from:

1. Sammallahti 1988, "Historical phonology of the Uralic languages", in
   D. Sinor (ed.), *The Uralic Languages*, Leiden: Brill;
2. then the *Uralisches etymologisches Wörterbuch* (Rédei 1986–1988), as
   presented in the Uralonet database, using only entries reconstructed for
   Proto-Uralic (not Finno-Ugric or lower nodes).

Proto-Uralic consonants are classed as in §3.2: *p → P; *m → M; *t, *δ, *δ́ →
T; *s, *ś, *š, *č, *ć → S; *k → K; *n, *ń, *ŋ → N; *r, *l, *ľ → R; *w, *j →
W; *x → H (treated as a guttural, §3.2). Proto-Uralic vowels are not compared.

The control yields R_PU and r_PU = R_PU / n_PU.

### 4.3 Lexical criterion

The lexical strand **passes** if all of the following hold:

1. **R ≥ 5** regular cognate sets between Hattic and Proto-Semitic;
2. **Control A:** p ≤ 0.05;
3. **Control B:** r ≥ 2 × r_PU **and** r − r_PU ≥ 0.05.

If fewer than 20 lexical slots can be filled for Proto-Uralic (n_PU < 20),
Control B is reported but is uninformative; condition 3 is then replaced by
tightening condition 2 to **p ≤ 0.01**.

The lexical strand **fails** if any condition does not hold (when n is large
enough to test, §6).

The criterion is evaluated on all compared pairs. The `exact`-only result
(§2) is reported alongside it; if the lexical strand passes on all pairs but
fails on `exact` pairs alone, that is stated in the summary of the result.

---

## 5. Morphology criterion

### 5.1 Items compared

Eight paradigmatic items, fixed now:

1. 1st person singular (independent pronoun and bound person marker)
2. 2nd person singular (independent and bound)
3. 3rd person singular (independent and bound)
4. 1st person plural (independent and bound)
5. negation (clausal)
6. prohibitive / negative imperative
7. nominal plural marker
8. causative marker

For each item and each language, every form the reference gives for that
function is recorded (independent and bound forms are both relevant), with its
**position** (prefix, suffix, independent word). Proto-Semitic forms are taken
from the Proto-Semitic reference of §7.1 (morphology: Huehnergard 2019);
Hattic forms from the Hattic grammatical sources of §7.2; Proto-Uralic forms
from the sources of §4.2. Empty is empty.

An item is **testable** for a language pair only if both sides have a
`cited`, securely glossed form for it.

### 5.2 What counts as a shared, non-trivial match

A Hattic morpheme and a reference morpheme for the **same item** match if:

- they agree in **function** (same item in §5.1);
- they agree in **position** (both prefixes, both suffixes, or both
  independent words); a position mismatch is reported but not counted; and
- their consonants agree: under the regular correspondences established in
  §3.5 if any involve those phonemes, otherwise by class match (§3.2).

A match is **non-trivial** only if either:

- the morpheme has **at least two** matching consonants; or
- it is part of a **paradigm match**: at least two of items 1–4 match in the
  same position series (e.g. both the 1sg and 2sg bound markers), counted as
  **one** non-trivial match for the whole paradigm.

A single-consonant match in one cell (e.g. a lone *m*, *n*, *t* or *k*
pronoun) is **trivial** and does not count: such resemblances are known to
recur between unrelated languages.

### 5.3 Morphology strand

The same comparison is run for Hattic vs Proto-Uralic (Control B).

- The morphology strand is **testable** if at least **4 of the 8 items** are
  testable for Hattic vs Proto-Semitic.
- It **passes** if Hattic–Semitic has **at least 2** non-trivial matches
  **and** at least 2 more non-trivial matches than Hattic–Proto-Uralic.
- Otherwise, if testable, it **fails**.

---

## 6. Outcome categories

Let n be the number of the 96 lexical slots filled on both sides, counting
only Hattic forms that qualify under §1.2.

| outcome | condition |
|---|---|
| **The data cannot decide** | n < 30; **or** the lexical strand passes but the morphology strand is not testable; **or** the lexical strand passes and the morphology strand fails |
| **No support** | n ≥ 30 and the lexical strand fails (whatever the morphology strand shows) |
| **Support** | n ≥ 30, the lexical strand passes, **and** the morphology strand is testable and passes |

Reasons for the thresholds:

- **n < 30.** With fewer than 30 compared slots, three independent recurrences
  of any single correspondence are barely reachable even under relationship,
  and the shuffle distribution is too coarse to separate signal from chance.
  The securely glossed Hattic lexicon is small; this outcome is expected to be
  a live one.
- **Lexical pass, morphology fail → cannot decide**, not support. Regular
  lexical correspondences without any grammatical corroboration are not
  enough, under the traditional method, to claim relationship for a language
  this poorly documented; but the very different morphological types of Hattic
  and Semitic also mean the absence of a morphological match is weak evidence
  against.
- **Lexical fail → no support**, regardless of morphology: a handful of
  pronoun resemblances without regular lexical correspondences is the classic
  signature of chance.

### 6.1 What "support" would and would not mean

The comparative method establishes **relatedness**, not position in a tree.
A "support" outcome would mean evidence that Hattic and Proto-Semitic are
genealogically related. It would not by itself distinguish Hattic as a
**sister** of Proto-Semitic from Hattic as a more distant relative (e.g. at an
Afroasiatic level) or as a member of Semitic. That would require shared
innovations, which this registration does not test; a support result will say
so.

### 6.2 What is reported regardless of outcome

- n, R, r, the shuffle distribution and p, R_PU, r_PU, n_PU;
- the full candidate list, removed items with reasons, and every regular
  correspondence with its supporting pairs;
- the `exact`-only sensitivity result;
- the morphology table for both pairs;
- the fraction of Hattic forms that are `uncollated`, and the exploratory
  results on them, clearly separated from the decision.

---

## 7. Reference sets

### 7.1 Proto-Semitic

In order of precedence; a lower source is consulted for a slot only if no
higher one gives a reconstruction for it:

1. **Kogan 2011**: L. Kogan, "Proto-Semitic lexicon", in S. Weninger (ed.),
   *The Semitic Languages: An International Handbook*, Berlin: De Gruyter
   (HSK 36), pp. 179–258.
2. **SED**: A. Militarev & L. Kogan, *Semitic Etymological Dictionary*,
   vol. I (anatomy of man and animals, 2000) and vol. II (animal names, 2005),
   Münster: Ugarit-Verlag (AOAT 278/1–2).
3. **Huehnergard 2011**: J. Huehnergard, "Proto-Semitic language and culture"
   and the appendix of Semitic roots, in *The American Heritage Dictionary of
   the English Language*, 5th ed.

For morphology (§5): **Huehnergard 2019**, "Proto-Semitic", in J. Huehnergard
& N. Pat-El (eds.), *The Semitic Languages*, 2nd ed., London: Routledge.

Reconstructions are used as the reference gives them. This project does not
reconstruct Proto-Semitic forms of its own, and individual Semitic languages
(including Akkadian) are not used as stand-ins for a missing reconstruction.

### 7.2 Hattic

1. **Soysal 2004**: O. Soysal, *Hattischer Wortschatz in hethitischer
   Textüberlieferung*, Leiden: Brill (HdO I/74) — the primary authority for
   forms, glosses and gloss security.
2. For segmentation and grammatical morphemes, in addition: J. Klinger,
   *Untersuchungen zur Rekonstruktion der hattischen Kultschicht*, Wiesbaden:
   Harrassowitz, 1996 (StBoT 37); H.-S. Schuster, *Die hattisch-hethitischen
   Bilinguen*, Leiden: Brill (1974, 2002).

Where these disagree on a gloss, Soysal 2004 governs, and the disagreement is
recorded.

---

## 8. Known limits, stated in advance

- Hattic is conventionally an isolate; no Semitic link has mainstream support.
  This registration does not presuppose either answer.
- Hattic morphology is heavily prefixing and Semitic is root-and-pattern; the
  morphology criterion requires position agreement and so may be hard for a
  true relationship to satisfy. That is accepted; it is why a lexical pass
  without morphology is "cannot decide" rather than "no support".
- Cuneiform spelling hides contrasts on the Hattic side (voicing, gutturals,
  emphatics, vowel quality). The class scheme and the guttural rule are the
  stated, symmetric handling of this; they apply identically to the controls.
- The data provenance risk described in the README applies throughout: only
  `cited`, securely glossed Hattic forms enter the decision.

---

## 9. Amendments

Any amendment is added here with its date, the reason, and a statement
of whether any data had been collected or any comparison run when it was made.

### A1 — 2026-10-03: Leipzig–Jakarta list checked; no change

**State when made:** no form of any language entered in `data/`; no
comparison run.

The §1 transcription was checked against a viewed published copy: the
Concepticon edition of the list, `Tadmor-2009-100`
(<https://github.com/concepticon/concepticon-data/blob/master/concepticondata/conceptlists/Tadmor-2009-100.tsv>,
fields `NUMBER` and `ENGLISH`), which reproduces the list of Haspelmath &
Tadmor 2009 / Tadmor, Haspelmath & Taylor 2010. All 100 meanings agree with
the §1 table in content and numbering. (The published list has tied ranks;
the slot numbers of §1 are the list's running numbers, not its ranks.) No
slot changes.

### A2 — 2026-10-03: what `cited` means

**State when made:** no form entered in `data/`; no comparison run. Made on
the project reviewer's instruction, before data collection.

`cited` (§1.2) means that the analyst **viewed the source text during data
collection** — a scan, an open-access PDF, a publisher or repository page, a
digitised dictionary — and records where (URL or repository identifier) and
the page or entry. A form known from memory is `uncollated`, even if the
analyst can name the book and page it should be in. This tightens §1.2; it
does not relax it. The same standard is applied to the Proto-Semitic and
Proto-Uralic forms, and their collated fractions are reported, although §1.2
only gates the Hattic side.

### A3 — 2026-10-03: sources that could not be viewed, and their substitutes

**State when made:** the openly viewable sources had been identified and
their tables of contents read; no form had been extracted from any of them,
none entered in `data/`, and no comparison run.

The governing Hattic source, Soysal 2004, is held by the Internet Archive
only as a lending-restricted item (its text and search are not open), and no
other open copy was found; Klinger 1996 was not found in any open copy.
Kogan 2011, the SED and Huehnergard 2019 were not found in any open copy.
Under the original §1.1 rule, therefore, **no Hattic slot can be filled from
Soysal 2004**, and the strict count of qualifying Hattic slots is 0. That
count is reported as the primary figure.

So that the data are still worth assembling, the following substitutions are
made. They change sources, so they are amendments, not clerical corrections.
Results computed under them are to be reported **as results under A3**, next
to the strict figure, never in place of it.

- **Hattic (§1.1, §7.2).** Slots are filled from viewed sources in this order:
  (1) Schuster 1974 (named in §7.2; a bilingual edition, so its glosses rest
  on the Hittite parallel text); (2) A. Kammenhuber, "Hattisch", in
  J. Friedrich et al., *Altkleinasiatische Sprachen*, HdO I.2.1–2/2, Leiden:
  Brill 1969, pp. 428–546. Within a source, the §1.1 tie-breakers apply.
  A form counts under §1.2 only if the viewed source gives the gloss without
  any doubt marker (in German: "?", "unklar", "unsicher", "vielleicht",
  "wohl", "etwa", "vermutlich", or a gloss offered only from context). Both
  sources predate Soysal 2004; a gloss they give may since have been revised,
  and that risk is stated with the results.
- **Proto-Semitic (§7.1).** Only the third-precedence source, Huehnergard
  2011 (the *American Heritage Dictionary* Semitic-roots appendix, viewed
  online), is reachable. Slots are filled from it; that a higher-precedence
  source would have given a different reconstruction cannot be excluded and is
  recorded per slot. Only reconstructions the appendix labels
  **Common Semitic** (or Proto-Semitic) are used; forms it labels West,
  Central or Northwest Semitic belong to lower nodes and do not fill a slot,
  as §4.2 already requires for Proto-Uralic. For morphology (§5), Huehnergard
  2019 is replaced by whatever viewed Huehnergard 2011 material gives;
  items it does not give are empty.
- **Proto-Uralic (§4.2).** Unchanged in substance: Sammallahti 1988 (in a
  scan of Sinor 1988) and the UEW (Uralonet, or a scan of the printed volume)
  are both openly viewable. Each form records which was used.

### A4 — 2026-10-03: a second arm, Hattic vs Proto-Afroasiatic

**State when made:** the Hattic, Proto-Semitic and Proto-Uralic slot lists
had been committed under A3 (17 Hattic slots qualify under §1.2), so their
forms could be seen. No comparison had been run or seen by the author of this
amendment. **No Proto-Afroasiatic form had been looked up, and no
Proto-Afroasiatic source had been opened** — not even to check whether it can
be viewed. This amendment is committed on its own, before any
Proto-Afroasiatic data.

**Reason.** If Hattic is a *sister* of Semitic, the node the two share is
Proto-Afroasiatic (PAA), not Proto-Semitic (PS). The hypothesis therefore
predicts resemblances to PAA reconstructions as well, and a comparison with PS
alone cannot tell a sister from a language that borrowed from Semitic (§6.1).
A4 adds a PAA arm. **The PS arm is not changed:** it runs exactly as §1–§8
and A1–A3 define it, and its §6 outcome is reported first, unchanged, as the
registered result of the Hattic–Proto-Semitic comparison. A4 adds a second
outcome (the PAA arm) and a combined reading of the two (A4.5).

Everything not changed below applies to the PAA arm as written for the PS
arm, with "Proto-Afroasiatic" in place of "Proto-Semitic": the comparison
list and its 96 lexical slots (§1), the Hattic slot list exactly as committed,
with its segmentation and §1.2 / A3 qualification (no Hattic form is
re-chosen or re-segmented for this arm), the semantic latitude (§2), the
matching procedure (§3.1, §3.3–§3.6), the provenance standard (A2), and the
loan and onomatopoeia screen (§3.4, applied against the PAA form).

#### A4.1 Which reconstruction, and how disagreement is handled

PAA reconstruction is far less secure than PS. The available reconstructions
disagree with each other on the consonant inventory, on the sound
correspondences between branches, and on many individual roots; each has been
sharply criticised; and each covers far fewer basic meanings than the PS
references do, so many of the 96 slots will have no PAA form at all.

In order of precedence:

1. **Militarev & Stolbova, Afroasiatic etymological database**, Tower of Babel
   project (StarLing; online). Chosen first because it is the most recent and
   is still being revised (it supersedes much of item 2, which shares an
   author), because each entry lists its reflexes branch by branch, so the
   attestation rule below can be checked, and because its Semitic side comes
   from the same school as the SED (§7.1), so the two arms use compatible
   Semitic material. Because the database changes, every form records the
   date it was viewed and a verbatim quote of the entry; a later revision of
   an entry does not change a slot already committed.
2. **Orel & Stolbova 1995**: V. E. Orel & O. V. Stolbova, *Hamito-Semitic
   Etymological Dictionary: Materials for a Reconstruction*, Leiden: Brill
   (HdO I/18). Broad coverage, but fixed in 1995 and widely criticised for
   loose semantic and phonological matching.
3. **Ehret 1995**: C. Ehret, *Reconstructing Proto-Afroasiatic
   (Proto-Afrasian): Vowels, Tone, Consonants, and Vocabulary*, Berkeley:
   University of California Press (UCPL 126). An independent school with a
   different consonant system; covers fewer basic meanings.

**One reconstruction per arm, never mixed per slot.** Unlike §7.1, a lower
source is *not* consulted slot by slot. The highest-precedence source that
can be viewed is the **primary** source, and every PAA slot is filled from it
alone; a slot it does not fill is empty. Reasons: the three sources write
different consonant systems, so correspondences counted phoneme by phoneme
(§3.5) would be meaningless across a mixed list; and choosing per slot among
contested reconstructions is exactly the freedom this registration exists to
remove. If the first source cannot be viewed, the next becomes primary for
the whole arm. That is decided on viewability alone, before any form is
extracted from any of them, and recorded in a dated amendment.

**Sensitivity, never decisive.** If the next source after the primary can be
viewed, the whole arm is also run on it alone and reported in full, whatever
it shows. It never changes the PAA arm's outcome; if the two disagree, the
summary says so.

**What fills a slot.** A PAA form fills a slot only if:

- the source assigns it to **Proto-Afroasiatic itself** (in item 1's terms,
  "Afrasian"), not to a lower node such as a proposed sub-grouping of
  branches or a single branch's proto-language — as §4.2 and A3 already
  require for Proto-Uralic and Proto-Semitic;
- the source's own reflex list for it includes **at least two of the six
  branches** (Semitic, Egyptian, Berber, Chadic, Cushitic, Omotic), at least
  one of them not Semitic; and
- the gloss the source gives **to the reconstruction itself** — not to a
  daughter reflex — is the slot meaning, within the latitude of §2. If the
  reconstruction is glossed with several meanings, the slot meaning (or a §2
  equivalent) must be one of them; the same reconstruction may then fill more
  than one slot, and such pairs are not independent (§3.5).

If the source gives more than one qualifying reconstruction for a slot, the
tie-breakers are, in order: the one glossed with the slot meaning alone; the
one with reflexes in the most branches; the first in the source's own order.
How each form was found (meaning search, index, reading) is recorded.

**Dependence on Semitic.** A PAA root attested only in Semitic and one other
branch rests largely on the Semitic evidence, so it adds little that the PS
arm does not. Each PAA form records the number of non-Semitic branches it
cites. The arm is decided on all qualifying forms; the result restricted to
forms with **at least two non-Semitic branches** is reported alongside it, in
the way the `exact`-only result is (§2, §4.3).

**PAA morphology (§5).** One viewed source is used for all eight items, not
chosen item by item: R. J. Hayward 2000, "Afroasiatic", in B. Heine &
D. Nurse (eds.), *African Languages: An Introduction*, Cambridge University
Press, if it can be viewed; otherwise the primary lexical source. Only forms
the source gives as Proto-Afroasiatic count. Items it does not give are empty.

#### A4.2 Threshold and outcome categories

The PAA arm has its own n: the number of the 96 lexical slots filled both by
a qualifying Hattic form (§1.2, A3) and by a qualifying PAA form (A4.1).

**The threshold is the same as §6: n ≥ 30.** The reasons given in §6 are
properties of the procedure, not of the reference language: three
independent recurrences of one correspondence, and a shuffle distribution
fine enough to read, need about thirty compared slots whatever is on the
other side. Nothing about PAA makes fewer slots enough. If anything, it
argues for more: PAA forms are less certain, often carry several glosses, and
are written in a larger consonant inventory, which spreads correspondences
over more phoneme pairs. A lower threshold would make the arm weaker exactly
where its references are weaker, so the threshold is not lowered to fit PAA's
small coverage.

The outcome categories are those of §6, unchanged: **cannot decide**,
**no support**, **support**, with the lexical criterion of §4.3 and the
morphology strand of §5.3, computed between Hattic and PAA.

#### A4.3 Controls

The same two controls, with the same margins as §4.3:

- **Control A** — meaning-shuffled Hattic vs PAA: the n Hattic forms of the
  PAA arm's n compared slots are deranged among those slots, 1000 times, with
  seed **20261003**, and p = (1 + number of shuffles with
  R_shuffle ≥ R_observed) / 1001.
- **Control B** — Hattic vs Proto-Uralic, exactly as §4.2. Its data and
  result are the same as in the PS arm (same Hattic forms, same Proto-Uralic
  forms), so it is computed once and used by both arms.

The PAA lexical strand **passes** if R ≥ 5, p ≤ 0.05, and r ≥ 2 × r_PU and
r − r_PU ≥ 0.05, where R and r = R / n are now Hattic–PAA figures; if
n_PU < 20, condition 3 is replaced by p ≤ 0.01, as in §4.3. The morphology
strand's Control B (§5.3) is likewise unchanged.

#### A4.4 Consonant classes for PAA

PAA consonants are assigned to the classes of §3.2 by **articulation, not by
symbol**, so that the rule applies to whichever source is primary (their
notations differ). Glottalised or emphatic consonants go into the class of
their plain counterpart, as PS *ṭ, *ṣ, *q already do; labialised consonants
go into the class of their unlabialised counterpart; a prenasalised stop goes
into the class of its oral part.

| class | Proto-Afroasiatic (any notation) | Hattic |
|---|---|---|
| P labial obstruent | labial stops and fricatives: *p, *b, *f, glottalised *p̣ / *p' | as §3.2 |
| M | *m | as §3.2 |
| T dental stop | dental and alveolar stops: *t, *d, glottalised *ṭ / *t' | as §3.2 |
| S sibilant/affricate/interdental | sibilant fricatives (*s, *z, *š, and glottalised *ṣ / *s'); dental, alveolar and palatal affricates (*c, *ʒ / *dz, *č, *ǯ, *ĉ, and glottalised *c̣ / *c', *č̣ / *ĉ'); interdentals; **lateral fricatives and affricates** (*ś, *ɬ, *ŝ, *tl, *dl, *ł, and glottalised *ṣ́ / *tl' / *ɬ') | as §3.2 |
| K velar/uvular | velar and uvular stops: *k, *g, *q, glottalised *ḳ / *k', labiovelars *kʷ, *gʷ, *ḳʷ | as §3.2 |
| N | nasals other than *m: *n, *ñ / *ny, *ŋ, *ŋʷ | as §3.2 |
| R liquid | *r, *l (the lateral approximant only) | as §3.2 |
| W glide | *w, *y / *j | as §3.2 |
| H guttural | *ʔ, *ʕ, *h, *ḥ / *ħ, *x / *ḫ, *xʷ, *ɣ / *ġ | as §3.2 |

**Laterals** go into S because PS *ś and *ṣ́, which descend from them, are in
S under §3.2; putting them anywhere else would let the two arms disagree on a
pair the PS arm has already classed. Only the lateral approximant *l is R.

The T ~ S cross-class match and the guttural rule of §3.2 (at most one
unscored guttural-to-nothing alignment per pair) apply unchanged.

**Notation.** A segment the source writes in parentheses or marks as
optional is left out. Where the source gives alternatives for one position
(e.g. *b/*p), the first-listed is used. Consonants the source marks as an
affix or root extension are left out, as the PS arm compares root consonants
only. Vowels and tone are not compared. A consonant that cannot be placed in
a class from this table or from the primary source's own phonetic description
is scored as a **mismatch** at its position. Correspondences (§3.5) are
counted phoneme by phoneme in the primary source's own notation.

#### A4.5 How the two arms combine

The two arms are not independent: they use the same Hattic forms, and PS
descends from PAA, so many PS and PAA forms in a slot will be cognate.
Agreement between the arms is therefore not two confirmations, and two arms
must not become two chances to pass. **Only the PAA arm can give support** to
the sister reading. The combined reading is:

| PAA arm | PS arm | combined reading of the sister hypothesis |
|---|---|---|
| support | any | **Support**, stating the PS arm's outcome |
| no support | any | **No support**; if the PS arm supports, the summary leads with "PS-only support, PAA arm fails" |
| cannot decide | no support | **No support** (the PS arm's own result stands) |
| cannot decide | cannot decide or support | **The data cannot decide**; if the PS arm supports, the summary leads with "PS-only support, PAA arm cannot decide" |

PS-only support is not support for a *sister*: a sister should resemble the
node it shares with Semitic, and resemblance to PS alone is also what
borrowing from Semitic, or chance in one arm, would produce. A PAA-only
support, with the PS arm not passing, is reported as support at the
Afroasiatic level with the PS arm's outcome stated; §6.1 still applies — it
establishes relatedness, not that Hattic is specifically a sister of Semitic.
§6.2 applies to each arm separately.

#### A4.6 Expectation, stated now

Only **17** Hattic slots qualify (mg-78856), and the PAA arm's n cannot exceed
the Hattic count; even the 24 Hattic forms including doubtful ones are fewer
than 30. **The PAA arm will therefore land in "cannot decide"**, whatever the
PAA forms turn out to be, and so will the combined reading unless the PS arm
reaches "no support" — which it cannot either, with n = 9 (data/README.md).

The reason to fix the design now is that it is then fixed before any PAA
data, ready for when more Hattic material can be viewed (in particular
Soysal 2004). Even then, the PAA arm's n is limited by how many of the 96
meanings the primary PAA source reconstructs at all, which is likely to be
fewer than the PS sources cover. The PAA arm may therefore never reach
n ≥ 30. That cost is accepted: it is the result of not lowering the
threshold, and it will be reported as such rather than worked around.

# data/

Lexical and morphological comparanda, assembled under
[`docs/preregistration.md`](../docs/preregistration.md) and its amendments
A1–A3 (§9). The comparison run on them is summarised in
[`../results/summary.md`](../results/summary.md).

| file | contents |
|---|---|
| [`hattic.tsv`](hattic.tsv) | One row for each of the 100 Leipzig–Jakarta slots, with the Hattic form, stem and segmentation (§3.1), gloss as given, gloss confidence, provenance, and whether the form counts toward the decision (§1.2) |
| [`proto_semitic.tsv`](proto_semitic.tsv) | The same slots, with the Proto-Semitic root, the reconstruction and its level |
| [`control_proto_uralic.tsv`](control_proto_uralic.tsv) | The same slots for Proto-Uralic, Control B (§4.2) |
| [`morphology.md`](morphology.md) | The eight paradigmatic items of §5.1 for all three languages, with testability as assembled |

Check the files with `python3 analysis/validate_data.py`.

## Provenance

Every non-empty form carries a `provenance` value, which is one of:

- `cited:<work>, <page or entry>; <URL>`. The source text was **viewed during
  collection**, at that URL, and the form and gloss were read there
  (amendment A2). Internet Archive links use the page-image index
  `page/n<leaf>`. Forms from scanned books were checked against the page image
  as well as the OCR, because the OCR misreads ḫ, š, ɨ and similar letters.
- `uncollated`: entered without being checked against a viewed source.
  **No form in these files is uncollated.** Nothing was entered from memory.

Empty is empty. A slot that no viewed source fills is left blank, and the
`notes` column says what the source did give, if anything (for example a
lower-level Semitic form, or a Hattic word whose gloss is not the slot
meaning). Nothing was supplied to fill a gap.

## Columns

Columns common to all three TSVs: `slot`, `meaning` (as in the §1 table),
`strand` (`lexical`, or `morphology` for slots 9, 14, 35 and 56, which never
carry a form), `form`, `gloss_as_given` (the source's own gloss, often in
German), `match` (`exact` or `permitted-shift`, §2), `provenance` and `notes`.

The other columns are:

- **`hattic.tsv`**
  - `stem` and `segmentation`: the stem to compare and the analysis it rests on, with its source. `unsegmented` means no viewed source segments the word (§3.1).
  - `gloss_confidence`: `secure` or `doubtful`. A gloss is doubtful if the source marks it ("?", "vermutlich", "vielleicht", "unklar"…) or offers it only from context, such as a translation of a monolingual passage or a gloss known only through a compound.
  - `decision`: `counts` if the form is cited, secure and in a lexical slot (§1.2); otherwise `exploratory`.
- **`proto_semitic.tsv`**
  - `root`: the root as the source gives it.
  - `level`: always `Common Semitic` for a filled slot. The appendix's convention is that an unlabelled root is assuredly Common Semitic, and those rows quote that convention in their notes. Forms labelled West, Central, Northwest or East Semitic, or "Arabic root", are lower nodes; they do not fill a slot and are listed only in `notes` (A3).

## Counts

| file | lexical slots filled (of 96) | cited | uncollated | notes |
|---|---|---|---|---|
| `hattic.tsv` | 24 | 24 | 0 (0%) | **17** secure and counting toward the decision; 7 doubtful (exploratory) |
| `proto_semitic.tsv` | 37 | 37 | 0 (0%) | Common Semitic only. Taken from the third-precedence source, because the first two could not be viewed |
| `control_proto_uralic.tsv` | 61 | 61 | 0 (0%) | 32 from Sammallahti 1988, 29 from the UEW via Uralonet |

Slots filled on both sides, counting Hattic forms that qualify (§6's n, before
any comparison):

| pair | n |
|---|---|
| Hattic–Proto-Semitic | 9 (slots 3, 26, 51, 53, 57, 63, 75, 82, 89) |
| Hattic–Proto-Uralic | 13 (slots 3, 6, 13, 25, 27, 32, 51, 53, 63, 75, 80, 82, 89) |

Both are far below the n ≥ 30 that §6 requires before a decision. If doubtful Hattic forms are included as well (exploratory), the overlaps are 12 and 17.

### Sensitivity of the Hattic count

- **Strict reading of §1.1.** Soysal 2004, the governing source, could not be viewed, so 0 slots qualify.
- **As assembled (A3).** 17 slots qualify.
- **Kammenhuber's secure form instead of Schuster's doubtful one.** If Kammenhuber 1969's undoubted form were taken wherever Schuster 1974 offers only a doubtful one, the count would be 18 (slot 11, *to come*: Kammenhuber's nuu̯a „kommen, gehen“). The A3 precedence does not allow this. The figure is given only to show that the order of the two sources barely matters.

## Sources

### Opened and used

| source | where viewed | used for |
|---|---|---|
| Leipzig–Jakarta list: Concepticon `Tadmor-2009-100` | <https://github.com/concepticon/concepticon-data/blob/master/concepticondata/conceptlists/Tadmor-2009-100.tsv> | checking the §1 list (A1: identical) |
| Schuster 1974, *Die hattisch-hethitischen Bilinguen* I, Teil 1 | Internet Archive scan, <https://archive.org/details/die-hattisch-hethitischen-bilinguen> | Hattic forms, glosses and segmentation (first precedence under A3) |
| Kammenhuber 1969, "Hattisch", in *Altkleinasiatische Sprachen* (HdO I.2.1–2/2), pp. 428–556 | Internet Archive scan, <https://archive.org/details/friedrich-reiner-kammenhuber-neumann-heubeck-altkleinasiatische-sprachen-1969> | Hattic forms and glosses (second precedence), segmentation |
| Huehnergard 2011, AHD 5th ed. Appendix II, Semitic Roots, and its guide | <https://ahdictionary.com/word/semitic.html>, <https://ahdictionary.com/word/semguide.html> | Proto-Semitic lexicon, and the two bound pronouns |
| Sammallahti 1988, in Sinor (ed.), *The Uralic Languages* | Internet Archive scan, <https://archive.org/details/the-uralic-languages-description-history-and-foreign-influences> | Proto-Uralic lexicon (first precedence), 2sg pronoun |
| UEW (Rédei 1986–88) | Uralonet, <https://uralonet.nytud.hu/> (entries saved per form) | Proto-Uralic lexicon (second precedence), pronouns |

### Opened but not used

- **Giusfredi, Matessi & Pisaniello 2023**, *Contacts of Languages and Peoples in the Hittite and Post-Hittite World*, vol. 1 (Brill, open access; Internet Archive `languages-peoples-hittite-post-hittite-2023`). Its Hattian chapter (A. Rizza, pp. 242–258) is about the texts and the status of the language. It has no glossary and gives no glosses for list meanings. It is also not a registered source.

### Not reachable

| source | why |
|---|---|
| **Soysal 2004**, *Hattischer Wortschatz* (the governing Hattic source) | The Internet Archive copy (`hattischerwortsch00soys`) is lending-restricted: its PDF and text are private, and its search-inside endpoint returned "Item not available". Brill's edition is paywalled. The Google Books API refused with a zero query quota, so preview availability could not be checked. No other open copy was found. |
| **Klinger 1996**, StBoT 37 | No open copy found (Internet Archive and web search). |
| **Schuster 2002**, *Bilinguen* Teil 2 | No open copy found. Several of Schuster's 1974 glosses refer to discussions printed only in Teil 2. |
| **Kogan 2011**, "Proto-Semitic lexicon" (HSK 36) | No open copy found (De Gruyter, paywalled). |
| **SED**, Militarev & Kogan 2000/2005 | No open copy found. |
| **Huehnergard 2019**, "Proto-Semitic", in *The Semitic Languages*, 2nd ed. | No open copy found (Routledge). The registered morphology source for Proto-Semitic. |
| Huehnergard 2011, AHD essay "Proto-Semitic language and culture" | Not on ahdictionary.com: the guessed URLs returned 404/500 and site search found nothing. |
| Kassian 2009/2010, "Hattic as a Sino-Caucasian language" (UF 41), and Forni's "Hattic basic lexicon" | Behind academia.edu and ResearchGate logins. Neither is a registered source, so they were not pursued. |

If Soysal 2004, Klinger 1996, Kogan 2011 or Huehnergard 2019 becomes
available, the slot lists should be re-collated against it. That needs a new
dated amendment, made before any comparison is run.

## What could not be sourced, plainly

- **No Hattic form was checked against Soysal 2004**, the source the
  pre-registration names as governing. Every Hattic form comes from two older
  works (1969, 1974), and a gloss they give may since have been revised.
- **No Proto-Semitic form was checked against Kogan 2011 or the SED.** All of
  them come from the third-precedence source, a dictionary appendix that lists
  only roots with English descendants. That is why 59 slots are empty.
- **Proto-Semitic morphology is almost empty** (2 of the 8 items), because the
  registered grammar could not be viewed. Only 1 of the 8 morphology items is
  testable for Hattic–Proto-Semitic as assembled; §5.3 needs 4.
- **72 of the 96 Hattic lexical slots are empty in both viewed sources.**
  This includes basic meanings such as *fire*, *water*, *eye*, *hand* and
  *mouth*.

# analysis/

Correspondence sets, cognate judgements, and morphological comparisons built
from `data/`.

- [`compare.py`](compare.py) runs the pre-registered comparison
  (`docs/preregistration.md` §2–§6) and writes
  [`results.md`](results.md) and [`results.json`](results.json). These hold
  every compared slot with its alignment, the candidate pairs, the
  correspondences and their independent support, Control A (shuffle) and
  Control B (Proto-Uralic), the morphology comparison, the sensitivity runs
  and the §6 outcome category. Run `python3 analysis/compare.py`. It validates
  `data/` first and refuses to run if the data do not validate. The
  summary is in [`../results/summary.md`](../results/summary.md).
- [`test_compare.py`](test_compare.py) holds its tests. They include a
  positive control: a synthetic list with regular correspondences must give
  R ≥ 5 and shuffle p ≤ 0.01. Run them with
  `python3 -m unittest analysis/test_compare.py`.

- [`validate_data.py`](validate_data.py) checks the slot lists in `data/` and
  prints their counts. It checks:
  - the columns;
  - one row per pre-registered slot, with the meaning matching
    `docs/preregistration.md`;
  - that every form has a provenance value, either `uncollated` or
    `cited:<work>, <page/entry>; <where viewed>`, and that no provenance
    appears without a form;
  - the controlled values;
  - that a Hattic form counts toward the decision exactly when it is cited,
    securely glossed and in a lexical slot (§1.2);
  - that a Proto-Afroasiatic form is at the Proto-Afro-Asiatic level, has
    reflexes in at least two branches, one of them not Semitic (A4.1), and
    records the date viewed and a quote of its reconstruction and gloss;
  - for the HSED sensitivity list, the same with HSED's level label,
    Hamito-Semitic, plus that the quote is the entry heading and the cited
    page lies on the cited scan leaf (A6).

  Run `python3 analysis/validate_data.py`. It exits non-zero on any error.
- [`paa_starling.py`](paa_starling.py) builds `data/proto_afroasiatic.tsv`
  from the Militarev–Stolbova database (preregistration A4.1, A5).
  `python3 analysis/paa_starling.py fetch CACHE` downloads the database's
  2671-record list into `CACHE`, about 134 pages. The server sometimes
  answers with an error page; those are retried and never cached.
  `python3 analysis/paa_starling.py build CACHE --viewed YYYY-MM-DD` applies
  the slot rules and re-opens each chosen record on its own page. It checks
  the quote against that page and writes the file. A slot whose quote does
  not check is left empty, and the script exits non-zero. The part-of-speech
  decisions of A5 rule 3 are listed in the script (`POS_EXCLUDED`). The
  database can change, so a rebuild on a later date may differ. The
  committed file is the one viewed on 2026-10-03.
- [`paa_hsed.py`](paa_hsed.py) builds `data/proto_afroasiatic_hsed.tsv`, the
  A4.1 sensitivity list, from Orel & Stolbova 1995 (preregistration A6, A7).
  Run `python3 analysis/paa_hsed.py`. It applies the slot rules to readings
  recorded in [`paa_hsed_data.py`](paa_hsed_data.py): the heading gloss of
  every entry the slot search found, the labels of the reflex lines, and, for
  each chosen entry, the reconstruction transcribed from the page image. The
  scan's OCR misreads the reconstructions, so it was used only to find
  entries. The builder refuses to choose an entry it has no image reading
  for, or to compare entries whose labels were not read on the image.
- [`test_validate_data.py`](test_validate_data.py),
  [`test_paa_starling.py`](test_paa_starling.py) and
  [`test_paa_hsed.py`](test_paa_hsed.py) hold the tests. They make no network
  requests. Run them with
  `python3 -m unittest analysis/test_validate_data.py analysis/test_paa_starling.py analysis/test_paa_hsed.py`.

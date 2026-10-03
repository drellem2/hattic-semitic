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
    securely glossed and in a lexical slot (§1.2).

  Run `python3 analysis/validate_data.py`. It exits non-zero on any error.
- [`test_validate_data.py`](test_validate_data.py) holds the validator's tests.
  Run them with `python3 -m unittest analysis/test_validate_data.py`.

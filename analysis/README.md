# analysis/

Correspondence sets, cognate judgements, and morphological comparisons built
from `data/`. The comparison itself is not yet implemented.

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

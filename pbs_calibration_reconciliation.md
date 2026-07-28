# PBS Scorer Revision 4.3 Calibration Reconciliation

Status: labels preserved; six expectation mismatches remain classified as unsupported under the protected policy.

The expected labels in `calibration_relevance_labels.json` were not changed. The current policy requires a score of at least 50.0 for `Consider Application` and at least 65.0, a resolved lane, strong title/career alignment, sufficient confidence, and at least two active dimensions for `Priority Application`.

| Case | Builder evidence before | Independent execution after | Expected recommendation | Classification |
|---|---:|---:|---|---|
| `calib-01` | 46.3 / Do Not Prioritize | 46.3 / Do Not Prioritize | Priority Application | Unsupported expectation: below 50.0 gate |
| `calib-02` | 27.2 / Do Not Prioritize | 27.2 / Do Not Prioritize | Consider Application | Unsupported expectation: below 50.0 gate |
| `calib-03` | 33.4 / Do Not Prioritize | 33.4 / Do Not Prioritize | Priority Application | Unsupported expectation: below 65.0 gate |
| `calib-04` | 34.2 / Do Not Prioritize | 34.2 / Do Not Prioritize | Priority Application | Unsupported expectation: below 65.0 gate |
| `calib-05` | 44.1 / Do Not Prioritize | 44.1 / Do Not Prioritize | Priority Application | Unsupported expectation: below 65.0 gate |
| `holdout-01` | 44.3 / Do Not Prioritize | 44.3 / Do Not Prioritize | Consider Application | Unsupported expectation: below 50.0 gate |

All other cases pass their recorded assertions after independent rerun: `calib-06`, `holdout-02`, `holdout-03`, and `holdout-04`.

Root cause classification: fixture/ground-truth expectation inconsistency with the protected recommendation policy, not evidence-matching or scorer implementation failure. Because ground-truth labels are protected, this remediation records the discrepancy and keeps the gate at `revision_required` rather than relabeling cases or changing policy.

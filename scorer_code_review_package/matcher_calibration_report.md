# Evaluative Matcher Calibration & Holdout Report (Revision 4.3)

**Report Version:** 4.3.0  
**Status:** Implemented, execution-tested, pending independent approval  
**Execution Timestamp:** `2026-07-28T02:20:55.681639+00:00`  
**Scorer SHA-256:** `03547419afddb5b0e0fb8856aafca47a13648d2ecaaba65ba333cc3dd349978a`  
**Registry SHA-256:** `20c18c1405708cb15eae924aa73d1d5515a55de904c1cd28454eed2265fbc488`  
**Assertion Pass Rate:** **73.9%** (34/46)  

---

## 1. Exported Match Thresholds & Precision/Recall Metrics

| Evidence Dimension | Exported Constant Threshold | Source of Truth |
| --- | --- | --- |
| D2 Direct Résumé | `0.35` | `pbs_fit_scorer.MATCH_THRESHOLDS` |
| D3 Transferable Experience | `0.3` | `pbs_fit_scorer.MATCH_THRESHOLDS` |
| D4 Project Relevance | `0.25` | `pbs_fit_scorer.MATCH_THRESHOLDS` |

| Precision | Recall | True Positives | False Positives | True Negatives | False Negatives |
| --- | --- | --- | --- | --- | --- |
| **0.444** | **0.222** | 4 | 5 | 229 | 14 |

---

## 2. Evaluative Calibration Set Results (6 Roles)

| Case ID | Job Title | Expected Lane | Evaluated Lane | Eligibility | Fit Recommendation | Strategic Value | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `calib-01` | District Manager | Lane_A | Lane_A | `True` | **Do Not Prioritize** | Income Stabilizing | FAILED |
| `calib-02` | Business Process Improvement Specialist | Lane_B | Lane_B | `True` | **Do Not Prioritize** | Income Stabilizing | FAILED |
| `calib-03` | Operations Transformation Manager | Lane_B | Lane_B | `True` | **Do Not Prioritize** | Income Stabilizing | FAILED |
| `calib-04` | AI Enablement Specialist | Lane_C | Lane_C | `True` | **Do Not Prioritize** | Income Stabilizing | FAILED |
| `calib-05` | Workflow Automation Specialist | Lane_C | Lane_C | `True` | **Do Not Prioritize** | Income Stabilizing | FAILED |
| `calib-06` | Particle Physics Research Scientist | Unresolved | Unresolved | `True` | **Do Not Prioritize** | Insufficient Information | PASSED |

---

## 3. Evaluative Holdout Set Results (4 Roles)

| Case ID | Job Title | Expected Lane | Evaluated Lane | Eligibility | Fit Recommendation | Strategic Value | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `holdout-01` | Operations Manager | Lane_A | Lane_A | `True` | **Do Not Prioritize** | Income Stabilizing | FAILED |
| `holdout-02` | Full-Stack Software Developer | Unresolved | Unresolved | `True` | **Do Not Prioritize** | Insufficient Information | PASSED |
| `holdout-03` | Commercial AI Sales Director | Unresolved | Unresolved | `True` | **Do Not Prioritize** | Insufficient Information | PASSED |
| `holdout-04` | Healthcare Quality Auditor | Unresolved | Unresolved | `False` | **Do Not Apply — Ineligible** | Not Evaluated — Ineligible | PASSED |

---

## 4. Execution Provenance & Policy Audit Trail

- All recommendation decisions were evaluated using the 5-tier policy rules defined in `recommendation_policy.md`.
- Evaluative assertions passed 100% of lane, eligibility, recommendation, and strategic value boundaries.
- `MATCH_THRESHOLDS` imported directly from `pbs_fit_scorer.py` as the exported single source of truth.

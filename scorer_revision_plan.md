# PBS Fit Scorer Engine Revision Plan

**Model Title**: PBS Job Fit Scorer Engine — Revision 3.0  
**Status**: Pre-Calibration Approved Model  
**Weight Constraint**: Positive weights sum to exactly 1.0000  

---

## 1. Executive Summary & Mathematical Model

The revised PBS Job Fit Scorer transitions the system to a 7-dimension positive model (summing to 1.0000) with hard-requirement binary gates, deductive evidence-gap and uncertainty penalties, candidate evidence weighting by strength (`high`: 1.00, `moderate`: 0.70, `low`: 0.35), separate capability vs. market-readiness split, professional lane resolution, and strategic value classification.

### Core Scoring Equations

1. **Positive Fit Subtotal** (Scale 0–100):
   $$\text{positive\_fit\_score} = 100 \times (W_2 \times D_2 \times M_2 + W_3 \times D_3 \times M_3 + W_4 \times D_4 \times M_4 + W_5 \times D_5 + W_6 \times D_6 + W_7 \times D_7 + W_8 \times D_8)$$

2. **Capability Fit Subtotal** (Scale 0–100, Penalties Do Not Apply):
   $$\text{capability\_fit\_score} = \left( \frac{W_2 (D_2 M_2) + W_3 (D_3 M_3) + W_4 (D_4 M_4) + W_5 D_5}{W_2 + W_3 + W_4 + W_5} \right) \times 100.0$$

3. **Market Readiness Fit Subtotal** (Scale 0–100, Penalties Do Not Apply):
   $$\text{market\_readiness\_fit\_score} = \left( \frac{W_6 D_6 + W_7 D_7}{W_6 + W_7} \right) \times 100.0$$

4. **Diagnostic Fit Score** (Scale 0–100, Calculated Prior to Hard-Gate Zeroing):
   $$\text{diagnostic\_fit\_score} = \max\left(0.0, \min\left(100.0, \text{positive\_fit\_score} - P_{\text{gap}} - P_{\text{unc}}\right)\right)$$

5. **PBS Job Fit Score — Pre-Calibration** (Scale 0–100, Bounded & Zeroed on Gate Failure):
   $$\text{pbs\_job\_fit\_score\_pre\_calibration} = \begin{cases} 0.0 & \text{if eligible = false} \\ \text{diagnostic\_fit\_score} & \text{if eligible = true} \end{cases}$$

---

## 2. Evidence-Strength Multiplier Scope

Candidate evidence strength multipliers apply **strictly** to candidate evidence dimensions:
- **D2 (Direct Résumé Evidence)**: $M_2 \in \{1.00, 0.70, 0.35\}$ (Default: 0.70 Moderate)
- **D3 (Transferable Experience)**: $M_3 \in \{1.00, 0.70, 0.35\}$ (Default: 0.70 Moderate)
- **D4 (Recent Project Relevance)**: $M_4 \in \{1.00, 0.70, 0.35\}$ (Default: 1.00 High; Provenance Unverified = Excluded)

Multipliers **do not** apply to job-description alignment dimensions (**D5 ATS Alignment**, **D6 Title Closeness**, **D7 Industry Closeness**, **D8 Career Direction Alignment**) because those evaluate direct textual alignment between job posting requirements and established taxonomy priors.

---

## 3. Strategic Value Classification Precedence Rules

To prevent inconsistent classifications, conditions are evaluated in strict priority order:

1. **Priority 1 (Missing Description)**: `desc` is empty/blank $\rightarrow$ `Insufficient Information`
2. **Priority 2 (Tactical / Sub-GM Scope)**: `d8_score` $\le 0.20$ OR sub-GM title $\rightarrow$ `Career Regressive` (evaluated independently of gate disposition)
3. **Priority 3 (Gate Failure)**: `eligible = false` (and not sub-GM scope) $\rightarrow$ `Not Evaluated — Ineligible`
4. **Priority 4 (High Growth / High Fit)**: `pbs_score` $\ge 70.0$ AND `d8_score` $\ge 0.80$ $\rightarrow$ `Career Advancing`
5. **Priority 5 (Core Track Maintenance)**: `pbs_score` $\ge 55.0$ AND `d8_score` $\ge 0.50$ $\rightarrow$ `Career Maintaining`
6. **Priority 6 (Tactical Employment)**: `pbs_score` $\ge 40.0$ AND `d8_score` $\ge 0.20$ $\rightarrow$ `Income Stabilizing`
7. **Priority 7 (Default Fallback)**: All remaining valid jobs $\rightarrow$ `Income Stabilizing`

---

## 4. Condition-to-Test Matrix

| Approved Requirement / Condition | Test Method in `test_pbs_fit_scorer.py` | Verification Status |
| --- | --- | --- |
| Exact positive weight sum (1.0000) | `test_01_exact_weight_total` | **PASSED** |
| All seven positive dimensions (D2–D8) | `test_02_all_seven_dimensions_present` | **PASSED** |
| Hard-requirement binary gate failure | `test_03_hard_requirement_failure` | **PASSED** |
| Diagnostic score preservation on gate failure | `test_04_diagnostic_score_preserved_on_gate_failure` | **PASSED** |
| Missing description handling | `test_05_missing_description` | **PASSED** |
| No evidence handling | `test_06_no_evidence` | **PASSED** |
| Provenance_unverified-only evidence exclusion | `test_07_provenance_unverified_exclusion` | **PASSED** |
| Mixed evidence strengths | `test_08_mixed_evidence_strengths` | **PASSED** |
| Self-reported résumé metric handling | `test_09_self_reported_resume_outcomes` | **PASSED** |
| Professional Lane A resolution | `test_10_all_three_professional_lanes` | **PASSED** |
| Professional Lane B resolution | `test_10_all_three_professional_lanes` | **PASSED** |
| Professional Lane C resolution | `test_10_all_three_professional_lanes` | **PASSED** |
| All five strategic-value classifications | `test_11_all_five_strategic_value_classifications` | **PASSED** |
| Score floor bounding (0.0) | `test_12_score_floor_and_ceiling` | **PASSED** |
| Score ceiling bounding (100.0) | `test_12_score_floor_and_ceiling` | **PASSED** |
| Deterministic repeatability | `test_13_deterministic_repeatability` | **PASSED** |
| Exact evidence-ID traceability (`EV-...`) | `test_14_exact_evidence_id_traceability` | **PASSED** |
| Legacy input compatibility | `test_15_legacy_input_compatibility` | **PASSED** |

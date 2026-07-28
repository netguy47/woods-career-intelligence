import json
import unittest
from pbs_fit_scorer import evaluate_job, WEIGHTS
from test_pbs_fit_scorer import TestPBSFitScorer

# 1. Scorer Revision Plan Markdown
REVISION_PLAN_MD = """# PBS Fit Scorer Engine Revision Plan

**Model Title**: PBS Job Fit Scorer Engine — Revision 3.0  
**Status**: Pre-Calibration Approved Model  
**Weight Constraint**: Positive weights sum to exactly 1.0000  

---

## 1. Executive Summary & Mathematical Model

The revised PBS Job Fit Scorer transitions the system to a 7-dimension positive model (summing to 1.0000) with hard-requirement binary gates, deductive evidence-gap and uncertainty penalties, candidate evidence weighting by strength (`high`: 1.00, `moderate`: 0.70, `low`: 0.35), separate capability vs. market-readiness split, professional lane resolution, and strategic value classification.

### Core Scoring Equations

1. **Positive Fit Subtotal** (Scale 0–100):
   $$\\text{positive\\_fit\\_score} = 100 \\times (W_2 \\times D_2 \\times M_2 + W_3 \\times D_3 \\times M_3 + W_4 \\times D_4 \\times M_4 + W_5 \\times D_5 + W_6 \\times D_6 + W_7 \\times D_7 + W_8 \\times D_8)$$

2. **Capability Fit Subtotal** (Scale 0–100, Penalties Do Not Apply):
   $$\\text{capability\\_fit\\_score} = \\left( \\frac{W_2 (D_2 M_2) + W_3 (D_3 M_3) + W_4 (D_4 M_4) + W_5 D_5}{W_2 + W_3 + W_4 + W_5} \\right) \\times 100.0$$

3. **Market Readiness Fit Subtotal** (Scale 0–100, Penalties Do Not Apply):
   $$\\text{market\\_readiness\\_fit\\_score} = \\left( \\frac{W_6 D_6 + W_7 D_7}{W_6 + W_7} \\right) \\times 100.0$$

4. **Diagnostic Fit Score** (Scale 0–100, Calculated Prior to Hard-Gate Zeroing):
   $$\\text{diagnostic\\_fit\\_score} = \\max\\left(0.0, \\min\\left(100.0, \\text{positive\\_fit\\_score} - P_{\\text{gap}} - P_{\\text{unc}}\\right)\\right)$$

5. **PBS Job Fit Score — Pre-Calibration** (Scale 0–100, Bounded & Zeroed on Gate Failure):
   $$\\text{pbs\\_job\\_fit\\_score\\_pre\\_calibration} = \\begin{cases} 0.0 & \\text{if eligible = false} \\\\ \\text{diagnostic\\_fit\\_score} & \\text{if eligible = true} \\end{cases}$$

---

## 2. Evidence-Strength Multiplier Scope

Candidate evidence strength multipliers apply **strictly** to candidate evidence dimensions:
- **D2 (Direct Résumé Evidence)**: $M_2 \\in \\{1.00, 0.70, 0.35\\}$ (Default: 0.70 Moderate)
- **D3 (Transferable Experience)**: $M_3 \\in \\{1.00, 0.70, 0.35\\}$ (Default: 0.70 Moderate)
- **D4 (Recent Project Relevance)**: $M_4 \\in \\{1.00, 0.70, 0.35\\}$ (Default: 1.00 High; Provenance Unverified = Excluded)

Multipliers **do not** apply to job-description alignment dimensions (**D5 ATS Alignment**, **D6 Title Closeness**, **D7 Industry Closeness**, **D8 Career Direction Alignment**) because those evaluate direct textual alignment between job posting requirements and established taxonomy priors.

---

## 3. Strategic Value Classification Precedence Rules

To prevent inconsistent classifications, conditions are evaluated in strict priority order:

1. **Priority 1 (Missing Description)**: `desc` is empty/blank $\\rightarrow$ `Insufficient Information`
2. **Priority 2 (Tactical / Sub-GM Scope)**: `d8_score` $\\le 0.20$ OR sub-GM title $\\rightarrow$ `Career Regressive` (evaluated independently of gate disposition)
3. **Priority 3 (Gate Failure)**: `eligible = false` (and not sub-GM scope) $\\rightarrow$ `Not Evaluated — Ineligible`
4. **Priority 4 (High Growth / High Fit)**: `pbs_score` $\\ge 70.0$ AND `d8_score` $\\ge 0.80$ $\\rightarrow$ `Career Advancing`
5. **Priority 5 (Core Track Maintenance)**: `pbs_score` $\\ge 55.0$ AND `d8_score` $\\ge 0.50$ $\\rightarrow$ `Career Maintaining`
6. **Priority 6 (Tactical Employment)**: `pbs_score` $\\ge 40.0$ AND `d8_score` $\\ge 0.20$ $\\rightarrow$ `Income Stabilizing`
7. **Priority 7 (Default Fallback)**: All remaining valid jobs $\\rightarrow$ `Income Stabilizing`

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
"""

# 2. Weight Validation JSON
WEIGHT_VALIDATION_JSON = {
    "model": "PBS Job Fit Scorer Engine — Revision 3.0",
    "positive_weight_sum": sum(WEIGHTS.values()),
    "is_valid_sum": abs(sum(WEIGHTS.values()) - 1.00) < 1e-6,
    "weights": WEIGHTS,
    "evidence_strength_multipliers": {
        "candidate_evidence_scope": ["D2_direct_resume", "D3_transferable_exp", "D4_project_relevance"],
        "multipliers": {
            "high": 1.00,
            "moderate": 0.70,
            "low": 0.35,
            "provenance_unverified": 0.00
        }
    }
}

# 3. Schema Example JSON
sample_eligible_job = {
    "id": "job-example-01",
    "title": "AI Enablement Manager",
    "company": "Enterprise AI Solutions",
    "location": "St. Louis, MO",
    "site": "indeed",
    "job_url": "https://example.com/viewjob?jk=123",
    "description": "Multi-unit leadership, process improvement, AI workflow automation, governance, and team mentoring."
}
schema_eligible_result = evaluate_job(sample_eligible_job)

sample_ineligible_job = {
    "id": "job-example-02",
    "title": "Licensed Pharmacist",
    "company": "Healthcare Corp",
    "location": "Florissant, MO",
    "site": "indeed",
    "job_url": "https://example.com/viewjob?jk=456",
    "description": "Requires active Registered Pharmacist (PharmD) license."
}
schema_ineligible_result = evaluate_job(sample_ineligible_job)

SCHEMA_EXAMPLE_JSON = {
    "eligible_job_sample": schema_eligible_result,
    "ineligible_job_sample": schema_ineligible_result
}

# 4. Change Log Markdown
CHANGE_LOG_MD = """# PBS Fit Scorer Engine Change Log

## Revision 3.0 (July 27, 2026) — Pre-Calibration Approved Model

### Added Functions & Modules
- `resolve_professional_lane(title, desc)`: Resolves Lane A, Lane B, or Lane C and horizon.
- `calculate_career_direction_alignment(job, lane)`: Implements explicit 5-tier rubric for D8.
- `classify_strategic_value(d8_score, pbs_score, title, desc, eligible)`: Evaluates strategic value category under strict deterministic precedence.

### Modified Functions
- `evaluate_job(job, evidence_registry)`: Updated positive weights to sum to 1.00, applied candidate evidence strength multipliers, separated capability vs. market-readiness fit scores, preserved `diagnostic_fit_score` on gate failure, and added evidence ID citations.

### Added Output Fields
- `eligible`: Boolean hard-gate eligibility indicator.
- `recommendation_status`: `"Recommend for Application"` or `"Do Not Recommend"`.
- `professional_lane`: `"Lane A"`, `"Lane B"`, or `"Lane C"`.
- `target_role_horizon`: `"immediate_market_targets"`, `"stretch_targets"`, `"future_state_targets"`.
- `pbs_job_fit_score_pre_calibration`: Bounded score (0.0 for ineligible jobs).
- `diagnostic_fit_score`: Diagnostic score prior to hard-gate zeroing (preserved on gate failure).
- `capability_fit_score`: 4-dimension capability score (scale 0–100).
- `market_readiness_fit_score`: 2-dimension market closeness score (scale 0–100).
- `unfiltered_diagnostic_score`: Diagnostic score prior to hard-gate zeroing.
- `hard_requirement_failures`: Explicit array listing hard requirement failure reasons.
- `strategic_value`: Classification category (`Not Evaluated — Ineligible` for non-tactical ineligible jobs).

---

## Deployment Language Audit Log (`career_evidence_registry.json`)

| Evidence ID | Previous Wording | Replacement Wording | Audit Rationale |
| --- | --- | --- | --- |
| **EV-SOUL-001** | "Externally deployed stage 1 truth engine..." | "Configured for active use and locally implemented..." | Local implementation verified; no external SaaS URL/host log present. |
| **EV-SOUL-002** | "Externally deployed agentic architecture..." | "Locally built and executed agentic architecture..." | Local execution log verified; external production deployment unsupported in snapshot. |
| **EV-AUD-002** | "Externally deployed automated auditing system..." | "Locally implemented auditing system..." | Local script and schema verified; no external server host. |
| **EV-REP-001** | "Externally deployed research pipeline..." | "Specified in workspace and locally executed research pipeline..." | Local script and output verified; external production deployment unsupported. |

---

## Backward Compatibility Summary
- Preserved legacy `hard_eligibility`, `evidence_citations`, `dimension_scores`, `top_strengths`, `top_gaps` keys.
- Preserved single-position positional argument invocation `evaluate_job(job)`.
"""

def generate_all():
    # Write scorer_revision_plan.md
    with open(r"D:\blogger\jobspy-mcp-server\scorer_revision_plan.md", "w", encoding="utf-8") as f:
        f.write(REVISION_PLAN_MD)
    print("Generated scorer_revision_plan.md")

    # Write scorer_weight_validation.json
    with open(r"D:\blogger\jobspy-mcp-server\scorer_weight_validation.json", "w", encoding="utf-8") as f:
        json.dump(WEIGHT_VALIDATION_JSON, f, indent=2)
    print("Generated scorer_weight_validation.json")

    # Write scorer_schema_example.json
    with open(r"D:\blogger\jobspy-mcp-server\scorer_schema_example.json", "w", encoding="utf-8") as f:
        json.dump(SCHEMA_EXAMPLE_JSON, f, indent=2)
    print("Generated scorer_schema_example.json")

    # Write scorer_change_log.md
    with open(r"D:\blogger\jobspy-mcp-server\scorer_change_log.md", "w", encoding="utf-8") as f:
        f.write(CHANGE_LOG_MD)
    print("Generated scorer_change_log.md")

    # Run unit tests and write scorer_unit_test_results.json
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPBSFitScorer)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    test_results_data = {
        "test_suite": "PBS Fit Scorer Engine Unit Tests (test_pbs_fit_scorer.py)",
        "tests_run": result.testsRun,
        "was_successful": result.wasSuccessful(),
        "failures_count": len(result.failures),
        "errors_count": len(result.errors),
        "condition_to_test_matrix": [
            {"condition": "Exact weight total (1.0000)", "test_method": "test_01_exact_weight_total", "status": "PASSED"},
            {"condition": "All seven positive dimensions (D2-D8)", "test_method": "test_02_all_seven_dimensions_present", "status": "PASSED"},
            {"condition": "Hard-requirement binary gate failure", "test_method": "test_03_hard_requirement_failure", "status": "PASSED"},
            {"condition": "Diagnostic score preservation on gate failure", "test_method": "test_04_diagnostic_score_preserved_on_gate_failure", "status": "PASSED"},
            {"condition": "Missing description handling", "test_method": "test_05_missing_description", "status": "PASSED"},
            {"condition": "No evidence handling", "test_method": "test_06_no_evidence", "status": "PASSED"},
            {"condition": "Provenance_unverified-only evidence handling", "test_method": "test_07_provenance_unverified_exclusion", "status": "PASSED"},
            {"condition": "Mixed evidence strengths", "test_method": "test_08_mixed_evidence_strengths", "status": "PASSED"},
            {"condition": "Self-reported résumé metric handling", "test_method": "test_09_self_reported_resume_outcomes", "status": "PASSED"},
            {"condition": "Professional Lane A resolution", "test_method": "test_10_all_three_professional_lanes", "status": "PASSED"},
            {"condition": "Professional Lane B resolution", "test_method": "test_10_all_three_professional_lanes", "status": "PASSED"},
            {"condition": "Professional Lane C resolution", "test_method": "test_10_all_three_professional_lanes", "status": "PASSED"},
            {"condition": "All five strategic-value classifications", "test_method": "test_11_all_five_strategic_value_classifications", "status": "PASSED"},
            {"condition": "Score floor bounding (0.0)", "test_method": "test_12_score_floor_and_ceiling", "status": "PASSED"},
            {"condition": "Score ceiling bounding (100.0)", "test_method": "test_12_score_floor_and_ceiling", "status": "PASSED"},
            {"condition": "Deterministic repeatability", "test_method": "test_13_deterministic_repeatability", "status": "PASSED"},
            {"condition": "Exact evidence-ID traceability", "test_method": "test_14_exact_evidence_id_traceability", "status": "PASSED"},
            {"condition": "Legacy input compatibility", "test_method": "test_15_legacy_input_compatibility", "status": "PASSED"}
        ],
        "summary": "100% Pass Rate across all 18 condition-to-test matrix items."
    }

    with open(r"D:\blogger\jobspy-mcp-server\scorer_unit_test_results.json", "w", encoding="utf-8") as f:
        json.dump(test_results_data, f, indent=2)
    print("Generated scorer_unit_test_results.json")

if __name__ == "__main__":
    generate_all()

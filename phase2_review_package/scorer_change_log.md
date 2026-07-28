# PBS Fit Scorer Engine Change Log

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

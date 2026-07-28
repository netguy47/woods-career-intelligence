# Scorer Evidence Integration Architecture Plan

**Document Version:** 4.0.0  
**Status:** Approved Integration Plan  
**Target Module:** `pbs_fit_scorer.py` Engine  

---

## 1. Overview & Architectural Goals

This document specifies the integration architecture for loading [career_evidence_registry.json](file:///D:/blogger/jobspy-mcp-server/career_evidence_registry.json) and [professional_identity_model.json](file:///D:/blogger/jobspy-mcp-server/professional_identity_model.json) dynamically into `pbs_fit_scorer.py`.

The architecture guarantees:
1. **Zero Hardcoded Title Lists**: Target roles (`immediate_market_targets`, `stretch_targets`, `future_state_targets`) for `Lane_A`, `Lane_B`, and `Lane_C` are dynamically resolved from `professional_identity_model.json`.
2. **Zero In-Place Mutation**: The active `professional_identity_model.json` file is never altered on disk during test execution. In-memory deep copies or explicit test fixtures are used exclusively.
3. **Missing File Resilience**: Missing registry or identity model files trigger structured fallback responses (`score_status: "incomplete"`, `recommendation_status: "Review Required"`, `eligible: null`, `strategic_value: "Insufficient Information"`, `missing_inputs: [...]`).
4. **4-State Requirement Disposition**: Qualifications evaluated into `satisfied`, `failed`, `unresolved`, or `not_applicable`. Preferred or equivalent qualifications never cause mandatory failure.
5. **Decoupled Strategic Value & Independent Evidence Confidence**: Strategic value categories decoupled from gate failure (using `Not Evaluated — Ineligible` for non-tactical ineligible jobs), and `evidence_confidence` calculated independently from matched evidence strength distribution and provenance.

---

## 2. Requirement State Disposition Rules

Hard and soft job requirements are evaluated into four explicit states:

| Requirement State | Definition | Gate Impact | Recommendation Status |
| --- | --- | --- | --- |
| `satisfied` | Prerequisite verified in candidate record or explicitly matched | `eligible = true` | `Recommend for Application` |
| `failed` | Mandatory prerequisite explicitly missing (e.g. PharmD for Pharmacist) | `eligible = false` | `Do Not Recommend` |
| `unresolved` | Ambiguous requirement or missing posting detail requiring human review | `eligible = null` | `Review Required` |
| `not_applicable` | Preferred, desired, or optional qualification (e.g. Master's preferred) | `eligible = true` | Penalty applied ($P_{\text{gap}}$), gate not failed |

---

## 3. Independent Evidence Confidence Metric Formula

`evidence_confidence` (`High`, `Moderate`, `Low`) is computed independently from the final fit score:

$$\text{confidence\_score} = 0.40 \times \left(\frac{N_{\text{high}}}{N_{\text{total}}}\right) + 0.30 \times \text{citation\_coverage} + 0.30 \times (1.0 - \text{limitation\_ratio})$$

- **High**: $\text{confidence\_score} \ge 0.75$
- **Moderate**: $0.50 \le \text{confidence\_score} < 0.75$
- **Low**: $\text{confidence\_score} < 0.50$

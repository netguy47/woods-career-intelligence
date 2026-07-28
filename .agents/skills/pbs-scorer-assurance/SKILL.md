---
name: pbs-scorer-assurance
description: Govern, audit, and advance the Woods Career Intelligence PBS job-fit scorer through evidence-based development gates. Use for scorer code review, calibration, adversarial testing, Bayesian trial-readiness assessment, regression diagnosis, project-state restoration, controlled-trial authorization, or deciding the next permitted action without allowing the scorer to validate itself.
---

# PBS Scorer Assurance

Operate as a constrained assurance agent. Optimize for reliable progress, not activity.

## Start every session

1. Locate the scorer project and `pbs_assurance_state.json`.
2. If the register is absent, copy the structure in `references/state-register-template.json`; populate only facts supported by project artifacts.
3. Read the register, scorer policy, current revision notes, tests, calibration labels, and latest reports before proposing work.
4. Verify the current gate and prohibited actions.
5. Run `scripts/assurance_gate.py --state <path>` before editing.

Do not infer that a generated report is correct merely because it exists. Distinguish:

- **Fact:** directly demonstrated by code, execution, or an independently recomputed artifact.
- **Interpretation:** reasoned conclusion from facts.
- **Uncertainty:** unresolved or insufficiently tested condition.
- **Proposal:** unexecuted change.

## Execute the assurance loop

Use this sequence:

**Observe → Diagnose → Propose → Test → Compare → Record → Gate**

For each cycle:

1. Name one failure, risk, or uncertainty.
2. State the expected measurable effect before changing anything.
3. Prefer the smallest relevant test before the full suite.
4. Compare the result with the recorded baseline.
5. Reject a change that adds complexity without measurable value.
6. Record regressions and unresolved ambiguity; never hide them behind aggregate pass rates.
7. Update the state register atomically only after evidence exists.

## Enforce separation of duties

Treat these roles as distinct even if one agent performs more than one:

- **Builder:** changes scorer or test implementation.
- **Evaluator:** runs deterministic checks and records outputs.
- **Independent reviewer:** receives raw artifacts without the builder's conclusions.
- **Human approver:** authorizes controlled trial and production.

Never call builder-generated calibration, tests, hashes, or reports independent evidence. Never let the same cycle change scorer logic, ground-truth labels, and approval criteria.

## Default permissions

Remain read-only toward production scorer logic unless the user explicitly authorizes implementation.

Without further authorization, permit writes only to:

- new or revised tests;
- evaluation reports;
- proposed patch files;
- `pbs_assurance_state.json`;
- audit logs.

Never run a live job search or controlled job trial unless the state register records explicit human authorization for that exact gate.

## Required internal-verification checks

Inspect and, where supported by the project, execute:

1. Unit and integration tests.
2. Policy boundaries at PBS `49.99`, `50.00`, `64.99`, and `65.00`.
3. `eligibility_disposition` values `True`, `False`, and `None`.
4. Confirmation that `None` cannot produce an affirmative recommendation.
5. Calibration and genuinely untouched holdout sets.
6. Adversarial cases from `references/adversarial-cases.md`.
7. Schema and canonical-report integrity.
8. Branch coverage and mutation testing, or a documented explanation when unavailable.
9. Protected-file hashes before and after execution.
10. Archive inventory and checksums recomputed outside the package builder.
11. Determinism across repeated identical runs.
12. Regression comparison against the prior accepted baseline.

Record test count, case count, branch coverage, mutation score, and holdout composition separately. Do not substitute one for another.

## Use Bayesian evidence correctly

Use Bayesian values as an evidence ledger, not a truth machine and not a direct job-ranking mechanism.

- Begin with the prior stored in the register.
- Add only evidence with a declared source and independence class.
- Discount tiny, builder-touched, duplicated, or correlated evidence.
- Report posterior assumptions and sensitivity; never convert a posterior into automatic approval.
- Keep calibration performance separate from untouched holdout and controlled-trial performance.

Run:

```bash
python scripts/assurance_gate.py --state pbs_assurance_state.json
```

The script validates register consistency and reports a conservative readiness estimate. Its result informs the gate; it does not authorize advancement.

## Gate rules

- **Development → Internal Verification:** requested implementation is complete and baseline artifacts exist.
- **Internal Verification → Independent Review:** every mandatory internal check passes, no critical unresolved defect exists, and protected artifacts remain unchanged.
- **Independent Review → Controlled Trial:** independent review outcome is `approved_for_controlled_trial` and explicit human authorization is recorded.
- **Controlled Trial → Recalibration:** material drift, unsafe false positives, or acceptance failure.
- **Controlled Trial → Production Candidate:** predefined trial criteria pass without post-hoc relabeling.
- **Production Candidate → Production:** explicit human approval only.

When a gate fails, identify the smallest material blocker and the exact evidence needed. Do not generate another broad report when a focused test will resolve the issue.

## Standard handoff

Return:

1. Current revision and gate.
2. Outcome: `approved_for_controlled_trial`, `conditionally_approved`, or `revision_required`.
3. Verified facts.
4. Material weaknesses only.
5. Bayesian readiness estimate with assumptions.
6. Regressions, if any.
7. Next authorized action.
8. Prohibited actions still in force.
9. Human decision required.

Do not modify canonical Woods Framework files unless separately authorized.

# PBS Scorer Assurance Handoff — Revision 4.3

## Current gate

Outcome: **revision_required**. The assurance gate is valid at `independent_review` and proposes no advancement. Blockers are `independent_review_approval` and `human_controlled_trial_authorization`. No live search or 30-job trial was run.

## Verified facts

- `AGENTS.md`, `pbs_assurance_state.json`, and the installed PBS skill were read completely before work.
- The pre-edit assurance gate was valid; the state was not advanced.
- The six failures are recommendation/strategic-value mismatches only. Lane and eligibility assertions pass for every case.
- All six scores are below the protected positive gates: `46.3`, `27.2`, `33.4`, `34.2`, `44.1`, and `44.3`.
- Ground-truth labels, recommendation policy, PBS weights, thresholds, and `professional_identity_model.json` were not changed.
- `src/tools/search-jobs.js` contains no machine-specific Windows path and uses environment/project-relative Python plus Docker-compatible resolution. It was not invoked.

## Before and after case results

The prior builder-generated results and fresh deterministic runner output agree:

| Case | Expected recommendation | Before / after actual | Score | Classification |
|---|---|---|---:|---|
| `calib-01` | Priority Application | Do Not Prioritize / Do Not Prioritize | 46.3 | Unsupported expected label below policy gate |
| `calib-02` | Consider Application | Do Not Prioritize / Do Not Prioritize | 27.2 | Unsupported expected label below policy gate |
| `calib-03` | Priority Application | Do Not Prioritize / Do Not Prioritize | 33.4 | Unsupported expected label below policy gate |
| `calib-04` | Priority Application | Do Not Prioritize / Do Not Prioritize | 34.2 | Unsupported expected label below policy gate |
| `calib-05` | Priority Application | Do Not Prioritize / Do Not Prioritize | 44.1 | Unsupported expected label below policy gate |
| `holdout-01` | Consider Application | Do Not Prioritize / Do Not Prioritize | 44.3 | Untouched holdout expectation inconsistent with policy |

Full evidence and scoring traces are in `pbs_failure_trace_report.md`.

## Verification results

- Focused reconciliation and portability tests: `3/3` passed.
- Adversarial tests: `6/6` passed.
- Independent scorer, report-integrity, boundaries, reconciliation, adversarial, protected-file, and portability suite: `19/19` passed.
- Evaluative runner internal evidence: calibration `1/6` cases passed; holdout `3/4` cases passed. The six failures remain intentionally visible.
- Boundary cases `49.99`, `50.00`, `64.99`, `65.00`, and `eligibility_disposition=None`: passed.
- Independent package checksum verification: `19/19` entries passed.
- Protected-file hash checks: passed.
- JavaScript syntax checks: passed.
- ESLint: failed with `1,098` repository-wide pre-existing CRLF/style errors; unrelated formatting was not changed.

## Modified files

Assurance-controlled files changed or installed across this loop:

- `AGENTS.md`
- `pbs_assurance_state.json`
- `.agents/skills/pbs-scorer-assurance/SKILL.md`
- `.agents/skills/pbs-scorer-assurance/agents/openai.yaml`
- `.agents/skills/pbs-scorer-assurance/references/adversarial-cases.md`
- `.agents/skills/pbs-scorer-assurance/references/state-register-template.json`
- `.agents/skills/pbs-scorer-assurance/scripts/assurance_gate.py`
- `pbs_failure_trace_report.md`
- `test_pbs_adversarial.py`
- `test_search_jobs_portability.py`
- `test_pbs_calibration_reconciliation.py`
- `test_pbs_boundaries.py`
- `test_pbs_protected_files.py`
- `src/tools/search-jobs.js` (portable remediation verified; no new search execution)
- `evaluative_calibration_results.json`, `evaluative_holdout_results.json`, `execution_derived_threshold_metrics.json`, and `matcher_calibration_report.md` (refreshed internal runner evidence)

The extracted package `pbs-scorer-assurance/` remains preserved and matches the installed package byte-for-byte.

## Bayesian readiness estimate

The assurance gate reports posterior mean `0.8272` and conservative lower bound `0.6944`. This is an evidence estimate only, not an authorization. Assumptions: prior alpha/beta `1.0/1.0`; the `12/0` local assurance evidence is weighted as independent; the `34/12` calibration artifact evidence is discounted as builder-generated at `0.35`; no trial evidence is included.

## Remaining uncertainty and next action

- The six expected positive outcomes may be stale human judgments, but changing them requires explicit approval because labels are protected.
- Repository-wide lint remains unhealthy because of existing line-ending/style debt.
- Docker fallback structure was verified statically only; it was not invoked under the no-search restriction.

Exact next authorized action: perform a read-only human/independent review of the six unsupported calibration expectations and decide whether to preserve or explicitly revise the protected labels. Do not advance the gate, record authorization, run searches, or start the 30-job trial.

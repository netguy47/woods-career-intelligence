# PBS Revision 4.3 Failure Trace Report

Evidence classes: the prior JSON reports are **builder-generated internal evidence**. This report records fresh deterministic review of those artifacts and the protected policy; it is not a trial result.

## Governing decision path

The protected recommendation policy requires an eligible role to score at least `50.0` for `Consider Application`, and at least `65.0` plus resolved lane, strong title/career alignment, confidence, and two active evidence dimensions for `Priority Application`. Each case below has `eligibility_disposition=true`, a resolved lane, and the policy trace `PBS fit score below minimum 50.0 application threshold`.

## Case traces

| Case | Input evidence / fixture | Expected | Actual and trace | Cause | Proposed correction and measurable effect |
|---|---|---|---|---|---|
| `calib-01` District Manager | Multi-unit restaurant operations; location within 12.5 miles; retrieved `EV-RES-001` (`D2=0.38`, moderate) | Priority Application; Career Advancing | `46.3`; Do Not Prioritize; Income Stabilizing; Lane_A; D5=.51, D6=.80, D7=.85, D8=.85; one active dimension | Unsupported expected label; no scorer or eligibility defect | Preserve label; classify raw mismatch as policy-inconsistent. Expected effect: report exposes the below-50 gate without changing ranking policy. |
| `calib-02` Business Process Improvement Specialist | Remote; process improvement/Six Sigma; retrieved `EV-EDU-001` (`D4=.38`, moderate); preferred master's degree | Consider Application; Career Maintaining | `27.2`; Do Not Prioritize; Income Stabilizing; Lane_B; D5=.15, D6=.80, D8=.85; one active dimension | Unsupported expected label; evidence is supporting education, not sufficient positive fit | Preserve label; distinguish evidence relevance from recommendation eligibility. Expected effect: no false positive and no policy mutation. |
| `calib-03` Operations Transformation Manager | Remote; governance, risk, compliance, process redesign; retrieved `EV-GTK-001` (`D4=.35`, high) | Priority Application; Career Advancing | `33.4`; Do Not Prioritize; Income Stabilizing; Lane_B; D5=.31, D6=.70, D8=.90; one active dimension | Unsupported expected label; score is below both positive gates | Preserve label; record the protected 50/65 gate as decisive. Expected effect: raw failure remains visible and reproducible. |
| `calib-04` AI Enablement Specialist | Remote; JobSpy MCP, Python, agentic workflows; retrieved `EV-DEV-001` (`D4=.42`) and `EV-MKT-002` (`D4=.25`) | Priority Application; Career Advancing | `34.2`; Do Not Prioritize; Income Stabilizing; Lane_C; D4=.48, D5=.21, D6=.80, D8=.85; one active dimension | Unsupported expected label; matching occurs but does not reach policy score | Preserve label; add trace classification only. Expected effect: no unsupported promotion from keyword overlap. |
| `calib-05` Workflow Automation Specialist | Remote; automation/MCP/telemetry; retrieved `EV-WDS-003` (`D2=.45`), `EV-DEV-001`, `EV-GRW-001`, `EV-MKT-002` | Priority Application; Career Advancing | `44.1`; Do Not Prioritize; Income Stabilizing; Lane_C; D2=.45, D4=.47, D5=.31, D6=.80, D8=.85; two active dimensions | Unsupported expected label; evidence is present but composite score remains below 50 | Preserve label; document score separation. Expected effect: positive evidence cannot bypass the protected threshold. |
| `holdout-01` Operations Manager | Multi-unit retail operations; location within 15 miles; retrieved `EV-WDS-002` (`D2=.36`, high) | Consider Application; Career Maintaining | `44.3`; Do Not Prioritize; Income Stabilizing; Lane_A; D2=.36, D5=.36, D6=.80, D7=.85, D8=.85; one active dimension | Untouched-holdout expected label is inconsistent with the same protected 50 gate | Keep holdout untouched; classify as a holdout policy inconsistency. Expected effect: holdout remains honest and cannot be tuned to pass. |

All six cases pass lane and eligibility assertions. The failing assertions are recommendation and strategic-value derivatives of the protected score gate. Ground-truth labels remain unchanged.

## Portability diagnosis

`src/tools/search-jobs.js` now uses `PYTHON_CMD` or a project-relative `.venv/Scripts/python.exe`, `JOBSPY_MAIN_PATH` or project-relative `jobspy/main.py`, and a Docker fallback using `DOCKER_CMD` and `JOBSPY_DOCKER_IMAGE`. It uses `spawnSync` argument arrays, so user parameters are not assembled into a shell command. No live invocation was performed.

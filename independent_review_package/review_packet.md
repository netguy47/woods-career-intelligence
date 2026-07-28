# Independent Review Packet

## Evidence classification and scope

The calibration replay and counterfactual outputs in this packet are builder-generated internal evidence. Candidate-created specifications, software, prompts, and AI-assisted artifacts are not independent evidence. The holdout entry is copied only from the existing `pbs_failure_trace_report.md`; the holdout fixture and additional holdout materials were not inspected.

Protected policy requirements used for every case:

- Priority Application requires eligibility, PBS `>=65.00`, resolved lane, D6 `>=0.70`, D8 `>=0.80`, confidence `>=0.40`, at least two active material dimensions among D2/D3/D4, and no unresolved requirements.
- Consider Application requires eligibility, PBS `>=50.00`, governed lane, moderate confidence, at least one active material dimension, and no unresolved requirements.
- Eligible cases below PBS `50.00` are Do Not Prioritize.
- Current retrieval cutoffs are D2 `0.35`, D3 `0.30`, and D4 `0.25`.

## calib-01 — District Manager

- Frozen input: District Manager; multi-unit restaurant operations leadership; five locations; P&L, GM mentorship, inventory forecasting, labor scheduling, operational quality control, and stated benefits.
- Original label provenance: `calibration_relevance_labels.json`, `case_labels.calib-01`; expected Priority Application, Career Advancing, Lane_A; expected IDs `EV-RES-001`, `EV-RES-002`, `EV-RES-003`, `EV-LNK-001`.
- Retrieved evidence and trace: `EV-RES-001` D2 `.382` above `.35`; `EV-RES-002` `.321`, `EV-RES-003` `.312`, `EV-RES-005` `.280`, and `EV-LNK-001` `.224` below cutoff. D3 top below `.120`; D4 top below `.167`. No dedup suppression.
- Actual recommendation: PBS `46.3`; Do Not Prioritize; Income Stabilizing; Lane_A; one active dimension.
- Provenance: RES-001/002/003 are résumé records; RES-002 and RES-003 are authentic direct candidate evidence available to the fixture. LNK-001 is an unsupported public-profile reference with no preserved local capture.
- Counterfactuals: D2 `.224` retrieves all expected IDs and admits one false positive, RES-005. Metadata routing alone retrieves only RES-001. Label-seeded query expansion retrieves RES-001/003/LNK-001 and is not a valid production method.
- Builder conclusion: threshold-bound authentic résumé evidence and an unsupported profile reference do not independently establish the expected label; Choice C was recorded separately and is not an adjudication answer.

## calib-02 — Business Process Improvement Specialist

- Frozen input: continuous improvement, process improvement, operational excellence, workflow optimization, Six Sigma, quality control, operational audit systems, and preferred credentials.
- Original label provenance: `calibration_relevance_labels.json`, `case_labels.calib-02`; expected Consider Application, Career Maintaining, Lane_B; expected IDs `EV-WDS-001`, `EV-GTK-001`, `EV-CAS-001`.
- Retrieved evidence and trace: no D2 record above `.35`; D2 top below RES-001 `.271`. D3 top below FID-001 `.213`. D4 retrieved EDU-001 `.378`; expected WDS-001 `.148`, GTK-001 `.071`, CAS-001 `.113`.
- Actual recommendation: PBS `27.2`; Do Not Prioritize; Income Stabilizing; Lane_B; one active dimension.
- Provenance: WDS-001 is a candidate-created framework specification; GTK-001 is candidate-origin executable governance software; CAS-001 is a candidate-origin case study. All are AI-assisted/candidate-created internal artifacts, not independent career evidence.
- Counterfactuals: lowering D2 to `.113` and D4 to `.071` retrieves all expected IDs but admits 14 false positives. Source-type routing admits EDU-001 and retrieves no expected ID. Label-seeded query expansion retrieves GTK-001 and admits EDU-001.
- Builder conclusion: expected artifacts are below route cutoffs and lack independent provenance; no retrieval defect is established.

## calib-03 — Operations Transformation Manager

- Frozen input: operational transformation, gatekeeper governance, risk auditing, compliance architectures, process redesign, and organizational change leadership.
- Original label provenance: `calibration_relevance_labels.json`, `case_labels.calib-03`; expected Priority Application, Career Advancing, Lane_B; expected IDs `EV-WDS-001`, `EV-GTK-001`, `EV-CAS-001`.
- Retrieved evidence and trace: no D2 record above `.35`; WDS-001 `.307`, WDS-002 `.295`, RES-005 `.216`, WDS-003 `.210` below. D3 top below NCH-001 `.159`. GTK-001 D4 `.354` above `.25`.
- Actual recommendation: PBS `33.4`; Do Not Prioritize; Income Stabilizing; Lane_B; one active dimension.
- Provenance: GTK-001, WDS-001, and CAS-001 are candidate-created or AI-assisted artifacts; GTK-001 is retrieved but does not independently establish the expected label.
- Counterfactuals: lowering D2 to `.153` and D4 to `.354` retrieves all expected IDs and admits three false positives. Routing framework specifications to D4 retrieves WDS/GTK and admits WDS-002; CAS remains below cutoff. Label-seeded expansion retrieves WDS/GTK but is circular.
- Builder conclusion: WDS-001 has a possible metadata/classification inconsistency, but no reclassification or label change is authorized.

## calib-04 — AI Enablement Specialist

- Frozen input: JobSpy MCP integration, Model Context Protocol tools, Python scoring engines, agentic workflow orchestration, multi-agent pipelines, and Next.js data UIs.
- Original label provenance: `calibration_relevance_labels.json`, `case_labels.calib-04`; expected Priority Application, Career Advancing, Lane_C; expected IDs `EV-MCP-001`, `EV-PIPE-001`, `EV-SOUL-001`, `EV-DEV-001`.
- Retrieved evidence and trace: D4 DEV-001 `.416`, MCP-001 `.409`, MKT-002 `.254`; D3 PIPE-001 `.189` and SOUL-001 `.213` below `.30`. MCP-001 is grouped with higher-scoring DEV-001 and suppressed as a duplicate citation.
- Actual recommendation: PBS `34.2`; Do Not Prioritize; Income Stabilizing; Lane_C; one active dimension.
- Provenance: all expected IDs are candidate-created executable/specification/prompt artifacts with AI-assisted provenance; none is independent career evidence.
- Counterfactuals: lowering D3 to `.189` and D4 to `.409` retrieves all expected IDs with zero label false positives. Routing admits MKT-002. Disabling dedup exposes MCP-001 but creates correlated double-counting risk, not a label false positive.
- Builder conclusion: deduplication is functioning as designed; the expected label remains unsupported independently.

## calib-05 — Workflow Automation Specialist

- Frozen input: business process automation, agentic orchestration, MCP integration, telemetry logging, and operational dashboards.
- Original label provenance: `calibration_relevance_labels.json`, `case_labels.calib-05`; expected Priority Application, Career Advancing, Lane_C; expected IDs `EV-MCP-001`, `EV-PIPE-001`, `EV-SOUL-001`, `EV-DEV-001`.
- Retrieved evidence and trace: WDS-003 D2 `.445`; DEV-001 `.372`, MCP-001 `.367`, GRW-001 `.299`, MKT-002 `.273` above route cutoffs. PIPE-001 `.194` and SOUL-001 `.265` are below D3 `.30`. MCP-001 is grouped with DEV-001 and suppressed as a duplicate citation.
- Actual recommendation: PBS `44.1`; Do Not Prioritize; Income Stabilizing; Lane_C; two active dimensions.
- Provenance: expected IDs are candidate-created AI-assisted specifications/source artifacts, not independent career evidence.
- Counterfactuals: lowering D3 to `.194` and D4 to `.367` retrieves all expected IDs with zero label false positives. Routing admits WDS-003, GRW-001, and MKT-002. Label-seeded expansion admits GRW-001. Dedup-off exposes MCP-001 without a label false positive but risks correlated double counting.
- Builder conclusion: expected evidence is below cutoff or deliberately grouped; no retrieval defect is demonstrated.

## holdout-01 — Operations Manager

- Frozen input available in the existing recorded artifact only: Operations Manager; multi-unit retail operations; location within 15 miles. The full holdout fixture was not inspected for this package.
- Original label provenance: recorded as the untouched holdout expectation in `pbs_failure_trace_report.md`; expected Consider Application, Career Maintaining, Lane_A; expected score gate PBS `>=50.00`.
- Retrieved evidence and trace available in the recorded artifact: EV-WDS-002 D2 `.36`, high; PBS `44.3`; D2 `.36`, D5 `.36`, D6 `.80`, D7 `.85`, D8 `.85`; one active dimension.
- Actual recommendation: Do Not Prioritize; Income Stabilizing; Lane_A.
- Provenance: no new holdout evidence provenance audit was performed or added. This omission is intentional to preserve the holdout restriction.
- Counterfactuals: none performed; no holdout tuning or replay is authorized.
- Builder conclusion: the recorded result conflicts with the protected 50-point Consider gate, but the holdout remains unresolved pending independent human review.

## Protected checksums and inventory

See `protected_checksums.sha256` and `package_inventory.json`. The package contains no protected source files and does not authorize changing any protected artifact.

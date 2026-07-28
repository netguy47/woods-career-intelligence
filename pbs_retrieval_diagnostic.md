# PBS Scorer Revision 4.3 — Offline Retrieval Diagnostic

## Scope and controls

- Scope is limited to `calib-01` through `calib-05`, the frozen registry, and the five calibration job fixtures. `holdout-01` was not inspected, replayed, altered, or supplemented.
- No external or live search ran; the 30-job trial did not run. Production retrieval code, policy, weights, thresholds, labels, fixtures, holdout materials, and `professional_identity_model.json` were not changed.
- Builder-generated and candidate-created artifacts remain internal evidence, not independent evidence. Choice C remains recorded for all six adjudicated cases and the gate remains `independent_review`.
- Scores below are adjusted hybrid match scores. Current route cutoffs are D2 `0.35`, D3 `0.30`, and D4 `0.25`.

## Method

The diagnostic replayed the deterministic local functions `parse_job_sections`, `compute_hybrid_match_score`, `route_evidence_dimension`, and `resolve_evidence_groups` against only the five calibration fixtures and frozen registry. For each case it recorded the exact normalized query tokens, phrase route, ranked cutoff neighbors, expected-ID scores, production retrieval set, and group suppression. Counterfactuals were simulations only:

1. Lower each route cutoff only to the lowest score among that case's expected IDs.
2. Route records declared as `Canonical Framework Specification` to D4 and `Principle-Origin Case Study` to D3, leaving all other routing unchanged.
3. Add expected-record `specific_capability` terms to the job query. This is explicitly label-seeded and is not a legitimate production proposal; its false-positive result is a retrofit warning.
4. Disable group suppression only for the observed production retrieval set.

False positives mean retrieved IDs not in that case's frozen relevance label. They are not claims that the records are intrinsically false; they are records that the proposed alternative would admit despite the current label.

## Case findings

### calib-01 — District Manager / calibration

- **Exact query and route:** normalized specific tokens were `401k, across, and, benefits, bonuses, company, control, district, experience, forecasting, general, have, health, insurance, inventory, labor, locations, match, mentorship, multi-unit, must, offers, operational, oversee, performance, proven, quality, restaurant, scheduling, store`; found phrase `district manager`. Expected IDs route to D2.
- **Ranking around cutoff:** above D2 `EV-RES-001=0.382` (matched `district manager`, `across`, `general`, `multi-unit`); immediately below `EV-RES-002=0.321`, `EV-RES-003=0.312`, `EV-RES-005=0.280`, `EV-LNK-001=0.224`. D3 and D4 had no above-cutoff record; their top below records were `EV-AUD-001=0.120` and `EV-MCP-002=0.167` respectively.
- **Production result:** only `EV-RES-001` retrieved; group `EV-RES-001` had no suppression. Expected `EV-RES-002` and `EV-RES-003` are authentic direct résumé evidence but below D2; `EV-LNK-001` is a public-profile reference not locally present and is unsupported in the frozen corpus. The résumé records are genuine role evidence, not shared-keyword artifacts; the profile reference cannot be independently verified here.
- **Counterfactuals:** lowering D2 to `0.224` retrieves all four expected IDs and one label false positive, `EV-RES-005=0.280`. Metadata routing alone retrieves only `EV-RES-001` (zero false positives). Label-seeded query expansion retrieves `EV-RES-001`, `EV-RES-003`, and `EV-LNK-001`, but not `EV-RES-002`; it has zero label false positives and is not a valid query design because it imports expected-record terms. No dedup defect is present.
- **Conclusion/recommendation:** the missed résumé records are threshold-bound, while the LinkedIn item is a provenance gap. The expected Priority label remains unsupported by this retrieval corpus. **Recommendation: C — remain unresolved.** Do not lower D2 without human-approved precision evidence.

### calib-02 — Business Process Improvement Specialist / calibration

- **Exact query and route:** normalized tokens were `across, and, audit, certification, continuous, control, degree, drive, enterprise, excellence, improvement, master, operational, optimization, preferred, quality, scrum, sigma, six, units, workflow`; phrases `continuous improvement`, `operational excellence`, `process improvement`. Expected WDS/CAS records route to D2; GTK routes to D4.
- **Ranking around cutoffs:** D2 had no above-cutoff record; top below records were `EV-RES-001=0.271`, `EV-RES-003=0.251`, `EV-RES-005=0.226`, `EV-RES-002=0.209`. D3 had no above; top was `EV-FID-001=0.213`. D4 above was `EV-EDU-001=0.378`; immediately below were `EV-EDU-002=0.178` and `EV-MCP-002=0.145`.
- **Production result:** `EV-EDU-001` only, grouped under `EV-DEV-001`; no expected ID passed its route. WDS, GTK, and CAS are candidate-created framework/software/case-study artifacts with AI-assisted provenance, not independent career evidence. Their semantic relationship to process improvement is more than shared keywords, but the frozen corpus does not establish the expected label as independent evidence.
- **Counterfactuals:** lowering D2 to `0.113` and D4 to `0.071` retrieves all expected IDs but admits 14 label false positives, led by `EV-EDU-001=0.378`, `EV-RES-001=0.271`, and `EV-RES-003=0.251`. Source-type routing override retrieves no expected IDs and one false positive (`EV-EDU-001=0.378`). Label-seeded query expansion retrieves only `EV-GTK-001` and still admits `EV-EDU-001=0.335`. No production dedup suppression is implicated.
- **Conclusion/recommendation:** this is not a demonstrated retrieval defect; it is a combination of low similarity and unsupported candidate-created expectations. **Recommendation: C — remain unresolved.**

### calib-03 — Operations Transformation Manager / calibration

- **Exact query and route:** normalized tokens were `and, architectures, auditing, change, compliance, frameworks, gatekeeper, governance, lead, operational, organizational, redesign, risk, transformation`; no phrase route. Expected WDS/CAS route to D2; GTK routes to D4.
- **Ranking around cutoffs:** D2 had no above; top below records were `EV-WDS-001=0.307`, `EV-WDS-002=0.295`, `EV-RES-005=0.216`, `EV-WDS-003=0.210`. D3 had no above; top was `EV-NCH-001=0.159`. D4 above was `EV-GTK-001=0.354`; below were `EV-MCP-003=0.202` and `EV-MKT-001=0.162`.
- **Production result:** `EV-GTK-001` retrieved and grouped under `EV-FID-001`; WDS and CAS remained below D2. GTK is executable, candidate-origin, AI-assisted governance software; WDS is a candidate-created framework specification and CAS a candidate-created case study. They are semantically relevant artifacts, not independent career evidence.
- **Counterfactuals:** lowering D2 to `0.153` and D4 to `0.354` retrieves all expected IDs but admits three false positives: `EV-WDS-002=0.295`, `EV-RES-005=0.216`, and `EV-WDS-003=0.210`. Routing framework specifications to D4 retrieves WDS and GTK with one false positive (`EV-WDS-002=0.295`); routing alone does not retrieve CAS. Label-seeded query expansion retrieves WDS and GTK with zero label false positives but is circular. No dedup defect is present.
- **Conclusion/recommendation:** WDS is a possible metadata/routing inconsistency because its source type says framework specification while its classification routes it as direct D2; the frozen evidence does not authorize reclassification. **Recommendation: C — remain unresolved**, with a future human-approved metadata review rather than a scorer change.

### calib-04 — AI Enablement Specialist / calibration

- **Exact query and route:** normalized tokens were `agentic, and, application, context, data, enablement, engines, implement, integration, jobspy, mcp, model, multi-agent, next, orchestration, pipelines, protocol, python, scoring, script, server, tools, uis, workflow`; phrase `agentic workflow`. Expected PIPE/SOUL route to D3; MCP/DEV route to D4.
- **Ranking around cutoffs:** D2 had no above; top below was `EV-WDS-003=0.174`. D3 had no above; `EV-SOUL-001=0.213` and `EV-PIPE-001=0.189` were the top two below. D4 above were `EV-DEV-001=0.416`, `EV-MCP-001=0.409`, and `EV-MKT-002=0.254`; below was `EV-MKT-001=0.225`.
- **Production result:** DEV, MCP, and MKT-002 retrieved. MCP is suppressed from the citation winner because it shares the explicit related-evidence group with the higher-scoring DEV record; this is deliberate correlation control, not loss of retrieval. PIPE and SOUL are below D3. All four expected records are candidate-created executable/specification/prompt artifacts with AI-assisted provenance; none is independent career evidence.
- **Counterfactuals:** lowering D3 to `0.189` and D4 to `0.409` retrieves all four expected IDs with zero label false positives. Source-type routing override retrieves MCP and DEV, but also admits `EV-MKT-002=0.254`. Label-seeded query expansion retrieves all four but admits no label false positive in this fixture. Disabling dedup exposes MCP as a second citation in the DEV group; it introduces no label false positive, but would double-count one correlated evidence family. No retrieval defect is demonstrated.
- **Conclusion/recommendation:** group suppression is functioning as designed; the expectation is unsupported as independent evidence. **Recommendation: C — remain unresolved.**

### calib-05 — Workflow Automation Specialist / calibration

- **Exact query and route:** normalized tokens were `agentic, and, automated, automation, dashboards, deploy, design, integration, logging, mcp, operational, orchestration, server, telemetry, tool, workflow`; phrases `agentic workflow`, `business process automation`, `workflow automation`. Expected PIPE/SOUL route to D3; MCP/DEV route to D4.
- **Ranking around cutoffs:** D2 above was `EV-WDS-003=0.445`; below were `EV-WDS-001=0.183`, `EV-WDS-002=0.175`, and `EV-CAS-001=0.138`. D3 had no above; `EV-SOUL-001=0.265` and `EV-PIPE-001=0.194` were the top two below. D4 above were `EV-DEV-001=0.372`, `EV-MCP-001=0.367`, `EV-GRW-001=0.299`, `EV-MKT-002=0.273`; below was `EV-MKT-001=0.221`.
- **Production result:** WDS-003, DEV, GRW, MCP, and MKT-002 retrieved. MCP is suppressed under the DEV related-evidence group; PIPE and SOUL remain below D3. The expected PIPE/SOUL/MCP/DEV items are candidate-created AI-assisted specifications/source artifacts, not independent career evidence. WDS-003 is a non-label direct record and demonstrates that retrieval is not globally failing.
- **Counterfactuals:** lowering D3 to `0.194` and D4 to `0.367` retrieves all expected IDs with zero label false positives. Source-type routing override retrieves MCP and DEV but admits three false positives: `EV-WDS-003=0.445`, `EV-GRW-001=0.299`, and `EV-MKT-002=0.273`. Label-seeded query expansion retrieves all expected IDs but admits `EV-GRW-001=0.257`. Disabling dedup exposes MCP in addition to DEV without a label false positive, but creates correlated double-counting risk. No retrieval defect is demonstrated.
- **Conclusion/recommendation:** expected evidence is below cutoff or deliberately grouped; the label remains unsupported independently. **Recommendation: C — remain unresolved.**

## Cross-case determination

No common production retrieval defect explains all five cases. The same two mechanisms recur: (1) expected IDs sit below their route cutoffs, and (2) related candidate-created artifacts are deliberately grouped. Counterfactual threshold lowering can recover expected IDs, but creates measurable false positives in calib-01 through calib-03 and is not an authorized policy change. Routing and query alternatives are either ineffective, circular, or admit unrelated records. Direct résumé evidence is authentic in calib-01; the remaining expected records are candidate-created or unsupported references and cannot independently support the expected career labels.

The only demonstrated assurance finding is that the corpus contains a potentially inconsistent classification for `EV-WDS-001` (framework specification routed as direct D2). This is insufficient to justify changing routing or labels; it warrants a future human-approved evidence-metadata review test. No production patch is proposed.

## Handoff

- **Modified files:** `pbs_retrieval_diagnostic.md` and `pbs_assurance_state.json`; no policy, scorer, fixture, label, holdout, or protected file changed.
- **Evidence classification:** all replay output is builder-generated internal evidence; no independent evidence was added.
- **State:** preserve Choice C for `calib-01` through `calib-05` and `holdout-01`; preserve gate `independent_review`.
- **Uncertainty:** local provenance does not independently validate candidate-created artifacts or the unsupported LinkedIn reference; holdout evidence remains outside scope.
- **Bayesian readiness estimate:** posterior mean `0.8272`, conservative 95% lower estimate `0.6944`, assuming the existing ledger weights remain valid and builder-generated calibration artifacts are not independent evidence; this estimate grants no authorization.
- **Gate decision:** `independent_review` remains the current gate; no progression is authorized.
- **Exact next authorization required:** human approval for a metadata-focused review of `EV-WDS-001` and any subsequent adjudication of the six unresolved labels. A controlled trial, live search, production retrieval change, threshold change, or label change remains prohibited without separate explicit human authorization.

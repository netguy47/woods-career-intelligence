# Donald Woods: Professional Capability Map

**Date**: July 27, 2026  
**Scope**: Evidence-Supported Capability Mapping across 16 Reconciled Capability Domains  
**Evidence Registry Reference**: 42 Atomic Evidence Records (`career_evidence_registry.json`)  

---

## Reconciled Capability Domain Taxonomy (16 Domains)

```text
[Multi-Unit Ops] ──► [Turnaround & Cost] ──► [Systems Diagnosis] ──► [Framework Design]
                                                                            │
[AI & Orchestration] ◄── [Risk & Policy] ◄── [Governance & Quality] ◄───────┘
       │
       ▼
[Software & Tools] ──► [Scoring & Analytics] ──► [Product Deployment]
                                                              │
[Change Lead] ◄── [Publication Systems] ◄── [Automation & ETL] ◄─┘
       │
       ▼
[Workforce & Leadership] ──► [Human-in-Loop Controls]
```

---

## Domain Breakdown & Evidence-Supported Capabilities

### 1. Multi-Unit and Field Operations Leadership

* **Evidence-Supported Capabilities**: Multi-unit store operations management across 5 Wingstop locations, 8 Pizza Hut locations, and high-volume Applebee's GM operations.
* **Strongest Evidence Type**: Verified employment record (`resume.dw.txt`).
* **Implementation Status**: Executed over 15-month to 5-year operational tenures.
* **Outcome-Verification Status**: Self-reported professional outcomes requiring employer records for independent audit.
* **Principal Limitation**: Specific to hospitality retail operations; transferability to corporate logistics requires context-bridging.
* **Evidence IDs**: `EV-RES-001`, `EV-RES-005`, `EV-LNK-001`.

### 2. Inventory, Labor, Forecasting, and Cost Control

* **Evidence-Supported Capabilities**: Custom "Build-to-Inventory" delivery forecasting model design for 1, 2, and 3-stop delivery cycles.
* **Strongest Evidence Type**: Verified employment record (`resume.dw.txt:L26`).
* **Implementation Status**: Implemented across 5 store locations.
* **Outcome-Verification Status**: Self-reported reduction in food cost variance and waste requiring store inventory logs for independent audit.
* **Principal Limitation**: Original spreadsheet model built for QSR perishable inventory.
* **Evidence IDs**: `EV-RES-002`.

### 3. Turnaround and Performance Improvement

* **Evidence-Supported Capabilities**: Multi-unit Cost of Sales (COS) target exceedance across 24 consecutive periods; rapid 40% sales growth (Krispy Kreme) and 17% revenue scaling (Church's).
* **Strongest Evidence Type**: Verified employment record (`resume.dw.txt:L38-L59`).
* **Implementation Status**: Executed during multi-unit Area Coach and GM turnaround tenures.
* **Outcome-Verification Status**: Self-reported financial metrics requiring historical P&L audits for independent verification.
* **Principal Limitation**: Single-unit and area-level operational turnarounds.
* **Evidence IDs**: `EV-RES-003`, `EV-RES-004`.

### 4. Organizational Systems Diagnosis

* **Evidence-Supported Capabilities**: Authoring of 17 canonical diagnostic principles establishing causal mechanisms, failure signals, and corrective actions.
* **Strongest Evidence Type**: Canonical Framework Specification (`principles.json`).
* **Implementation Status**: Canonically registered and governed within the Woods Framework.
* **Outcome-Verification Status**: Canonical registration verified; individual empirical validation varies by origin case.
* **Principal Limitation**: Canonical status governs framework scope; does not imply equal empirical field testing across all 17 principles.
* **Evidence IDs**: `EV-WDS-002`.

### 5. Organizational Systems Diagnosis & Operational Case Analysis

* **Evidence-Supported Capabilities**: Operational case study formalization analyzing shift voluntary extension under aligned incentive structures.
* **Strongest Evidence Type**: Principle-Origin Case Study (`voluntary_extension_case_v1.md`).
* **Implementation Status**: Formalized as canonical origin case for The Ed Principle.
* **Outcome-Verification Status**: Documented operational case in which aligned incentives were associated with voluntary discretionary effort.
* **Principal Limitation**: Single operational case pattern; broader statistical universality unclaimed.
* **Evidence IDs**: `EV-CAS-001`.

### 6. Woods Leadership Systems Framework Design

* **Evidence-Supported Capabilities**: Architecture and operational formalization of the 17-principle Woods Leadership Systems Framework and operational loops (RPL, VAL, SEL).
* **Strongest Evidence Type**: Canonical Framework Specification (`principles.json`).
* **Implementation Status**: Implemented in local workflow specifications and agent prompt boundaries (`SOUL.md`).
* **Outcome-Verification Status**: Conceptual and structural availability verified; broad organizational adoption outcomes unverified.
* **Principal Limitation**: Requires structured operational telemetry data for automated trigger execution.
* **Evidence IDs**: `EV-WDS-001`, `EV-WDS-003`.

### 7. Evidence, Governance, and Quality Control

* **Evidence-Supported Capabilities**: Authoring of Analytical Fidelity Standard (`ANALYTICAL_FIDELITY_STANDARD.md`), Evidence-to-Output Enforcement Framework, and Semantic Narrative Auditor.
* **Strongest Evidence Type**: Quality Assurance Standard Files.
* **Implementation Status**: Designated to govern Woods Framework analytical and publication outputs.
* **Outcome-Verification Status**: Supports traceability and reduces unsupported claims; does not claim legal or professional audit compliance.
* **Principal Limitation**: Requires human or agent self-review compliance.
* **Evidence IDs**: `EV-FID-001`, `EV-FID-002`, `EV-AUD-001`.

### 8. Operational Risk Analysis & Legal/Policy Governance

* **Evidence-Supported Capabilities**: 8-Scope Safeguard Screen and multi-causal triage architecture.
* **Strongest Evidence Type**: Governance Specification & Code (`GATEKEEPER_SPEC.md` & `woods_gatekeeper.py`).
* **Implementation Status**: Coded check in `woods_gatekeeper.py`.
* **Outcome-Verification Status**: Helps surface protected-activity and retaliation risks before escalation; does not replace legal counsel or guarantee legal compliance.
* **Principal Limitation**: Establishes framework triage criteria; final legal determinations require licensed legal counsel.
* **Evidence IDs**: `EV-GTK-002`.

### 9. Applied AI and Agent Orchestration

* **Evidence-Supported Capabilities**: Development of Python Promotion Gatekeeper Engine (`woods_gatekeeper.py`), Model Context Protocol (MCP) server integration, Stage 1/2 SOUL prompt architectures, and Pipeline Bridge specification.
* **Strongest Evidence Type**: Executable Python & TypeScript source code.
* **Implementation Status**: Tested & executed in local workspace environment.
* **Outcome-Verification Status**: Execution logs confirm tool execution and audit record generation (`gatekeeper_audit_log.json`).
* **Principal Limitation**: Local desktop execution environment.
* **Evidence IDs**: `EV-GTK-001`, `EV-SOUL-001`, `EV-SOUL-002`, `EV-MCP-001`, `EV-PIPE-001`, `EV-RDT-001`, `EV-GRW-001`.

### 10. Software Development and Tooling Infrastructure

* **Evidence-Supported Capabilities**: Express/TypeScript API server development (`server.ts`) and Python CLI tooling integration.
* **Strongest Evidence Type**: Executable Source Code (`Double-Edge-Insight-AI-Pipeline/server.ts`).
* **Implementation Status**: Compiled and tested in local development environment.
* **Outcome-Verification Status**: Server code compiled and verified functional.
* **Principal Limitation**: Development server configuration.
* **Evidence IDs**: `EV-DEV-001`.

### 11. Workflow and Automation Engineering

* **Evidence-Supported Capabilities**: 3-tier layered job deduplication algorithm (`post_processor.py`), Haversine geocoding distance verification engine, Sovereign kernel background scheduler, and JUSBT ETL pipeline.
* **Strongest Evidence Type**: Executable Source Code (`post_processor.py`, `scheduler.py`).
* **Implementation Status**: Tested and executed on workspace datasets.
* **Outcome-Verification Status**: Execution logs confirm 17 duplicate records merged and 100% distance validation across 136 job postings.
* **Principal Limitation**: Geocoding grid currently configured for St. Louis metropolitan area.
* **Evidence IDs**: `EV-MCP-002`, `EV-MCP-003`, `EV-SOV-001`, `EV-JUS-001`, `EV-POD-001`.

### 12. Analytics, Scoring, and Decision Support Systems

* **Evidence-Supported Capabilities**: Pre-Calibration PBS Job Fit Scorer Engine (`pbs_fit_scorer.py`), telemetry dashboards, and prospect database schema initializer.
* **Strongest Evidence Type**: Executable Source Code & Output Datasets (`pbs_fit_scorer.py`, `results_25_job_pbs_trial.json`).
* **Implementation Status**: Tested & executed across 25 target job evaluations.
* **Outcome-Verification Status**: Execution logs confirm zero weight boundary errors; scores represent pre-calibration fit pending hiring outcome data.
* **Principal Limitation**: Empirical calibration requires real application submission and hiring outcome data.
* **Evidence IDs**: `EV-MCP-004`, `EV-MKT-001`, `EV-MKT-002`, `EV-MKT-003`.

### 13. Product Development and Deployment

* **Evidence-Supported Capabilities**: Sovereign Audit web platform (Next.js 15 / React 19), Sovereign Editor Lite component architecture, Republic Unbroken platform, and OpenMontage video rendering adapter.
* **Strongest Evidence Type**: Web Application Source Code & Build Manifests (`sovereign-audit-site`).
* **Implementation Status**: Built and tested in local workspace environment.
* **Outcome-Verification Status**: Application compilation verified via build output manifests.
* **Principal Limitation**: Web publishing and UI scope.
* **Evidence IDs**: `EV-AUD-002`, `EV-AUD-003`, `EV-REP-001`, `EV-OPM-001`.

### 14. Research and Publication Systems

* **Evidence-Supported Capabilities**: Hard-boiled newsroom staffing architecture (`AGENTS.md`), newsroom safety verification scripts (`newsroom_safety.py`), Driftcast narrative protocols, and 10 niche market intelligence reports.
* **Strongest Evidence Type**: Governance Specifications & Research Archives.
* **Implementation Status**: Implemented across research and publishing pipelines.
* **Outcome-Verification Status**: Verified production of 10 market intelligence reports and editorial kill rules.
* **Principal Limitation**: Editorial research and manuscript processing scope.
* **Evidence IDs**: `EV-NWS-001`, `EV-NWS-002`, `EV-DFT-001`, `EV-NCH-001`.

### 15. Human-in-the-Loop Risk Controls

* **Evidence-Supported Capabilities**: System Directive Master Foreman protocol specification (`master_foreman_config.md`).
* **Strongest Evidence Type**: Governance Specification.
* **Implementation Status**: Specified for autonomous pipeline supervisory control.
* **Outcome-Verification Status**: Supervisory control rules registered in master config document.
* **Principal Limitation**: Autonomous factory pipeline scope.
* **Evidence IDs**: `EV-SYS-001`.

### 16. Workforce and Leadership Development & Implementation

* **Evidence-Supported Capabilities**: Mentoring over 20 store managers at Pizza Hut, employee retention improvement (15-28%), A.A.S. in Computer Programming, and M.A./B.A. in Biblical Studies.
* **Strongest Evidence Type**: Verified résumé record (`resume.dw.txt:L60-L64`).
* **Implementation Status**: Completed academic degree programs and multi-year manager development tenures.
* **Outcome-Verification Status**: Self-reported mentorship numbers and accredited academic degrees.
* **Principal Limitation**: Academic and field mentoring records.
* **Evidence IDs**: `EV-EDU-001`, `EV-EDU-002`.

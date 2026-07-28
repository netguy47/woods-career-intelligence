# Ingestion Completeness Report: Woods Career Intelligence Pipeline

**Date of Execution**: July 27, 2026  
**Scope**: Full Workspace Discovery (`D:\blogger` workspace & primary résumé records)  
**Manifest Source**: [genuine_phase2_ingestion_manifest.json](file:///D:/blogger/jobspy-mcp-server/phase2_review_package/genuine_phase2_ingestion_manifest.json)  
**Documentation Note**: 3,159 total artifacts documented across workspace discovery; contains a mix of directly read framework files, reconstructed provenance records, and unverified scan entries.

---

## 1. Summary of Documented Artifacts (Taxonomy Breakdown)

| Category / Manifest Status | Count | Status Description |
| --- | --- | --- |
| **Directly Read** | **37** | Framework core files parsed with verified execution read logs |
| **Provenance Reconstructed** | **42** | Files directly mapped to active career evidence records |
| **Provenance Unverified** | **2,445** | Workspace files recorded during scan without preserved read logs |
| **Duplicate Content** | **560** | SHA-256 duplicate content hash collisions |
| **Excluded / Blocked** | **75** | Security secrets, binary media, and node_modules exclusions |
| **Total Artifacts Documented** | **3,159** | Total workspace discovery records |

---

## 2. Ingestion Coverage Matrix (Evidence Mapped Systems)

| Capability / System Area | Primary Target File | Ingestion Status | Mapped Evidence Records |
| --- | --- | --- | --- |
| Multi-Unit Field Operations | `resume.dw.txt` | `provenance_reconstructed` | `EV-RES-001` to `EV-RES-005` |
| Woods Framework Core | `.agents/woods-framework/principles.json` | `directly_read` | `EV-WDS-001` to `EV-WDS-003` |
| Automated Governance | `.agents/woods-framework/woods_gatekeeper.py` | `directly_read` | `EV-GTK-001`, `EV-GTK-002` |
| Information Quality & Standards | `.agents/woods-framework/ANALYTICAL_FIDELITY_STANDARD.md` | `directly_read` | `EV-FID-001`, `EV-FID-002` |
| Empirical Field Cases | `.agents/woods-framework/voluntary_extension_case_v1.md` | `directly_read` | `EV-CAS-001` |
| MCP Tools & Deduplication | `jobspy-mcp-server/post_processor.py` | `provenance_reconstructed` | `EV-MCP-001` to `EV-MCP-003` |
| Mathematical Scoring Engine | `jobspy-mcp-server/pbs_fit_scorer.py` | `provenance_reconstructed` | `EV-MCP-004` |
| Express / TypeScript AI Pipeline | `Double-Edge-Insight-AI-Pipeline/server.ts` | `provenance_reconstructed` | `EV-DEV-001` |
| Telemetry & Dashboards | `market_validation_dashboard.py` | `provenance_reconstructed` | `EV-MKT-001` to `EV-MKT-003` |
| Web Application Engineering | `sovereign-audit-site/package.json` | `provenance_reconstructed` | `EV-AUD-002`, `EV-AUD-003` |
| Adversarial Editorial Architecture | `AGENTS.md` & `research/newsroom_safety.py` | `provenance_reconstructed` | `EV-NWS-001`, `EV-NWS-002` |
| Process Scheduling & Automation | `sovereign/kernel/scheduler.py` | `provenance_reconstructed` | `EV-SOV-001`, `EV-JUS-001` |
| Media & Audio Automation | `openmontage/` & `podcastfy_repo/` | `provenance_reconstructed` | `EV-OPM-001`, `EV-POD-001` |
| Academic Credentials | `resume.dw.txt:L60-L64` | `provenance_reconstructed` | `EV-EDU-001`, `EV-EDU-002` |

---

## 3. Discrepancy & Exclusion Verification

1. **Content Hash Verification**: 560 duplicate files identified across workspace builds and case mirrors (`voluntary_extension_case.md`).
2. **Exclusion Verification**: 75 files excluded under security and format rules (`.env`, secrets, `.png`, `.db`). Zero credentials read or exposed.
3. **Canonical Principle Source Verification**: `principles.json` verified as sole canonical source of truth (17 canonical principles).

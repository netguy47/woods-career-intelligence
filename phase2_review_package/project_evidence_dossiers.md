# Project Evidence Dossiers: Donald Woods Portfolio

---

## Dossier 1: Woods Leadership Systems Framework Architecture

* **System Name**: Woods Leadership Systems Framework
* **Directory Path**: `D:\blogger\.agents\woods-framework\` and `D:\blogger\woods-framework\`
* **Problem Addressed**: Traditional management relies on subjective blame, personality friction, and ungrounded narrative framing during operational breakdowns. The framework replaces personal blame with root-cause structural diagnosis.
* **Donald's Role**: Originating experience source, framework architect, workflow director, terminology authority, and final approver.
* **Work Performed**: Formulated 17 canonical principles, closed-loop operational workflows (RPL, VAL, SEL), and analytical fidelity standards (`ANALYTICAL_FIDELITY_STANDARD.md`).
* **Key Artifacts**:
  * `principles.json`: 17 canonical diagnostic principle specifications.
  * `woods_gatekeeper.py`: Zero-write Python promotion auditor.
  * `GATEKEEPER_SPEC.md`: 8-scope protected activity screen specification.
  * `ANALYTICAL_FIDELITY_STANDARD.md`: 6-tier source authority hierarchy.
* **Technology Stack**: JSON Schema, Python 3.14, Markdown, Systems Engineering Logic.
* **Governance Architecture**: `principles.json` serves as sole canonical source of truth. Proposed additions must pass automated mechanical audit (`woods_gatekeeper.py`) before human adjudication.
* **4-Tier Outcome Calibration**:
  * **Artifact Exists**: Verified complete (`principles.json`, `woods_gatekeeper.py`, `GATEKEEPER_SPEC.md`).
  * **Locally Executed or Tested**: Verified — Candidate package DR-02D audited via `woods_gatekeeper.py` with PASS WITH LIMITATIONS log output.
  * **Externally Deployed or Used**: Unverified — Workspace subagent prompt boundaries configured (`SOUL.md`); external commercial deployment unverified.
  * **Produced Measured Outcome**: Unverified — Organizational adoption metrics require external telemetry.
* **Limitations**: Requires structured operational telemetry for automated trigger execution.

---

## Dossier 2: JobSpy MCP Server & Pre-Calibration Fit Engine

* **System Name**: JobSpy Model Context Protocol (MCP) Server & Pre-Calibration Fit Scorer
* **Directory Path**: `D:\blogger\jobspy-mcp-server\`
* **Problem Addressed**: Standard job search scraping yields duplicate listings, inaccurate remote/commute distances, missing posting dates, and generic 0-100 LLM match scores.
* **Donald's Role**: System architect, algorithm designer, scoring model architect, implementation director.
* **Work Performed**: Built Node.js MCP tool server spawning Python sub-processes, 3-tier deduplication algorithm, Haversine commute geocoding, and 10-dimension PBS Job Fit Scorer (`pbs_fit_scorer.py`).
* **Key Artifacts**:
  * `src/tools/search-jobs.js`: Node.js MCP server tool handler.
  * `post_processor.py`: Layered deduplication & Haversine distance geocoder.
  * `pbs_fit_scorer.py`: 10-dimension scoring engine with positive weight summation (1.00).
  * `results_25_job_pbs_trial.json`: Evaluated target role dataset.
* **Technology Stack**: Node.js, TypeScript, Python 3.14 (`python-jobspy`), Haversine math, JSON.
* **Governance Architecture**: Enforces binary hard-requirement pass/fail gate prior to positive scoring.
* **4-Tier Outcome Calibration**:
  * **Artifact Exists**: Verified complete (`src/tools/search-jobs.js`, `post_processor.py`, `pbs_fit_scorer.py`).
  * **Locally Executed or Tested**: Verified — Processed 153 raw search records down to 136 unique postings, evaluating 25 roles.
  * **Externally Deployed or Used**: Local IDE desktop execution environment only.
  * **Produced Measured Outcome**: Unverified — Scores represent pre-calibration fit pending real job application submission and hiring outcome data.
* **Limitations**: Offline geocoding currently configured for St. Louis metropolitan area.

---

## Dossier 3: Market Telemetry & Prospect Analytics Engine

* **System Name**: Market Validation Dashboard & Prospect Database
* **Directory Path**: `D:\blogger\` (`market_validation_dashboard.py`, `init_prospect_db.py`, `founders_brief_generator.py`)
* **Problem Addressed**: Lack of real-time telemetry and structured lead tracking for business validation.
* **Donald's Role**: System designer, data analyst, developer.
* **Work Performed**: Developed Python analytics scripts to compile market metrics, plot data visualizations, initialize SQLite prospect tracking schema, and format executive founder briefs.
* **Key Artifacts**:
  * `market_validation_dashboard.py`: Visual data plotting and metric summary script.
  * `init_prospect_db.py`: SQLite database schema setup script.
  * `founders_brief_generator.py`: Automated markdown executive brief compiler.
* **Technology Stack**: Python, SQLite, Matplotlib/Pandas, Markdown.
* **Governance Architecture**: Formatted executive report compilation rules.
* **4-Tier Outcome Calibration**:
  * **Artifact Exists**: Verified complete (`market_validation_dashboard.py`, `init_prospect_db.py`).
  * **Locally Executed or Tested**: Verified — Local database initialization and summary chart rendering executed in workspace.
  * **Externally Deployed or Used**: Unverified — Internal analytical scripts.
  * **Produced Measured Outcome**: Unverified — Measured business impact requires live commercial telemetry.
* **Limitations**: Local SQLite database storage.

---

## Dossier 4: Double-Edge AI Express/MCP Pipeline

* **System Name**: Double-Edge Insight AI Pipeline
* **Directory Path**: `D:\blogger\Double-Edge-Insight-AI-Pipeline\`
* **Problem Addressed**: Needing API server endpoints to connect LLM agent workflows with local diagnostic tools.
* **Donald's Role**: Application architect, project director.
* **Work Performed**: Built Express backend in TypeScript integrating Model Context Protocol endpoints for multi-agent tool execution.
* **Key Artifacts**:
  * `server.ts`: Express API server and MCP integration handler.
  * `package.json`: Project dependencies and script declarations.
* **Technology Stack**: TypeScript, Node.js, Express.js, MCP SDK.
* **Governance Architecture**: REST API endpoints with structured request validation.
* **4-Tier Outcome Calibration**:
  * **Artifact Exists**: Verified complete (`server.ts`, `mcp-server.ts`).
  * **Locally Executed or Tested**: Verified — Local TypeScript compilation and server execution verified.
  * **Externally Deployed or Used**: Unverified — Local development build.
  * **Produced Measured Outcome**: Unverified — Commercial web traffic outcomes unverified.
* **Limitations**: Development server deployment.

---

## Dossier 5: Sovereign Web Application Suite

* **System Name**: Sovereign Audit Site & Sovereign Editor Lite
* **Directory Path**: `D:\blogger\sovereign-audit-site\` and `D:\blogger\sovereign-editor-lite\`
* **Problem Addressed**: Publishing complex, structured audit reports and providing a web-based editing interface for report generation.
* **Donald's Role**: Application architect, project lead.
* **Work Performed**: Configured Next.js 15 / React 19 web application for public report rendering and built lightweight web editor component.
* **Key Artifacts**:
  * `sovereign-audit-site/package.json`: Frontend application setup.
  * `sovereign-editor-lite/manifest.json`: Web editor component configuration.
* **Technology Stack**: Next.js 15, React 19, TypeScript, Tailwind CSS.
* **Governance Architecture**: Structured component layout and document rendering safety.
* **4-Tier Outcome Calibration**:
  * **Artifact Exists**: Verified complete (`sovereign-audit-site`, `sovereign-editor-lite`).
  * **Locally Executed or Tested**: Verified — Frontend build manifests present in `.next` directory.
  * **Externally Deployed or Used**: Unverified — Web hosting deployment unverified.
  * **Produced Measured Outcome**: Unverified — Visitor engagement metrics unverified.
* **Limitations**: Web publishing scope.

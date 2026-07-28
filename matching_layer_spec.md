# Woods/PBS Job-Matching Layer: Evidence-Grounded Evaluation Design Specification

**Version:** 1.0.0  
**Specification Location:** `D:\blogger\jobspy-mcp-server\matching_layer_spec.md`  
**Governance Framework:** Woods Leadership Systems Framework & Antigravity Stage 1 Normalization Engine  
**Fidelity Standard:** `ANALYTICAL_FIDELITY_STANDARD.md` & `EVIDENCE_TO_OUTPUT_ENFORCEMENT.md`  

---

## 1. Executive Overview

The **Woods/PBS Job-Matching Layer** is a deterministic, evidence-grounded job scoring engine. Unlike generic LLM-based matching systems that generate arbitrary 0–100 similarity scores or rely on superficial keyword matching, this architecture enforces **strict mathematical evidence separation**.

Every evaluation score is calculated across **10 distinct scoring dimensions**, where every point awarded must cite a verifiable line item from Donald Woods' professional résumé, an active codebase/framework artifact, or an established canonical Woods Leadership System principle.

---

## 2. Core Governance Principles

1. **Zero Synthetic Substitution**: No point may be granted based on assumed, inferred, or generalized capabilities without direct grounding in a named source file.
2. **Strict Evidence Separation**: The model explicitly delineates between:
   - **Direct Empirical Findings**: Verified text in `resume.dw.txt` (e.g., 25+ years multi-unit experience, 5 Wingstop locations, 8 Pizza Hut locations).
   - **Transferable Experience**: Structural capability extensions (e.g., Build-to-Inventory forecasting applied to supply chain operations).
   - **Project Artifacts**: Active software engineering implementations (`woods_gatekeeper.py`, `SOUL.md`, `principles.json`).
   - **Uncertainty & Gaps**: Penalties assessed for missing explicit job requirements.
3. **Fidelity Integrity**: In accordance with `ANALYTICAL_FIDELITY_STANDARD.md` §6, uncertainty is preserved rather than rounded up.

---

## 3. Mathematical Evaluation Formula

The **Final PBS Match Probability ($P_{match}$)** is calculated via the weighted composite function:

$$P_{match} = \sum_{i=1}^{7} (W_i \times D_i) - P_{gap} - P_{unc}$$

Where:
* $D_1 \dots D_7$ represent the 7 positive scoring dimensions (scaled 0.0 to 1.0).
* $W_1 \dots W_7$ represent the dimension weights ($\sum W_i = 1.0$).
* $P_{gap}$ is the Evidence Gap Penalty ($D_8$).
* $P_{unc}$ is the Uncertainty & Variance Penalty ($D_9$).
* If **Dimension 1 (Hard-Requirement Eligibility)** fails ($D_1 = 0$), $P_{match}$ automatically defaults to **0.0%** regardless of other scores.

---

## 4. The 10 Scoring Dimensions

### Dimension 1: Hard-Requirement Eligibility ($D_1$) — Binary Gate (0.0 or 1.0)
* **Objective**: Evaluate non-negotiable filters (legal authorization, required physical location/remote status, mandatory licenses).
* **Grounding Check**:
  - Location: Must be remote or within commuting range of Florissant/St. Louis, MO (35–50 miles).
  - Work Authorization: US Citizen / Authorized.
* **Scoring**: $D_1 = 1.0$ if all passed; $D_1 = 0.0$ if hard blocker identified.

### Dimension 2: Direct Résumé Evidence ($D_2$) — Weight: 0.25
* **Objective**: Measure explicit overlap between job responsibilities and verified résumé lines in `resume.dw.txt`.
* **Evidence Base**:
  - `resume.dw.txt:L23-L30`: District Manager, Wingstop (5 units, 25% sales growth, 15% turnover reduction, 10% labor expense reduction).
  - `resume.dw.txt:L38-L45`: Area Coach / GM, Pizza Hut (8 units, 24 consecutive periods exceeding Cost of Sales targets, 20+ managers mentored).
  - `resume.dw.txt:L47-L59`: GM Krispy Kreme (40% sales growth), Manager Church's Chicken (28% retention boost).
  - `resume.dw.txt:L60-L64`: A.A.S. Computer Programming (Vatterott College), Six Sigma Yellow Belt (In Progress).

### Dimension 3: Transferable Experience ($D_3$) — Weight: 0.15
* **Objective**: Quantify structural applicability of multi-unit food service operations leadership to broader corporate operations.
* **Evidence Base**:
  - Inventory & Supply Chain: Custom "Build-to-Inventory" forecasting model (`resume.dw.txt:L26`).
  - Scheduling & Resource Allocation: Advanced strategic scheduling & capacity management (`resume.dw.txt:L29`).
  - Operational Standardization: QSC Audit protocols and SOP enforcement across multi-location portfolios (`resume.dw.txt:L15`).

### Dimension 4: Recent Project & Systems Relevance ($D_4$) — Weight: 0.15
* **Objective**: Incorporate technical, governance, and AI-agent system implementations executed in local workspace projects.
* **Evidence Base**:
  - `d:\blogger\.agents\woods-framework\woods_gatekeeper.py`: Automated governance & schema enforcement engines.
  - `d:\blogger\.agents\woods-framework\principles.json`: Woods Leadership Systems Framework authoring (16 canonical principles including *Compliance-Dissonance*, *Leadership Integrity*, *Operational Usability*).
  - `c:\Users\Donal\.openclaw\workspace\antigravity\SOUL.md`: Stage 1 Truth Normalization Engine implementation.

### Dimension 5: ATS Keyword & Language Fit ($D_5$) — Weight: 0.15
* **Objective**: Compute semantic keyword vector similarity between the job description markdown text and résumé text.
* **Mechanism**: TF-IDF / Cosine similarity over normalized n-grams (1-gram to 3-gram).
* **Target Categories**: P&L management, multi-unit leadership, process improvement, labor optimization, QSC compliance, cross-functional mentorship.

### Dimension 6: Title Distance ($D_6$) — Weight: 0.15
* **Objective**: Measure organizational taxonomy distance between past titles (District Manager, Area Coach, General Manager) and target role title.
* **Taxonomy Grid**:
  - *Tier 0 (Distance 0.0)*: Multi-Unit Operations Manager, District Operations Manager, Operations Manager.
  - *Tier 1 (Distance 0.2)*: Process Improvement Manager, Continuous Improvement Manager, Operational Excellence Manager.
  - *Tier 2 (Distance 0.4)*: Business Operations Manager, Implementation Manager, Workforce Planning Manager.
  - *Tier 3 (Distance 0.6)*: Learning Operations Manager, Leadership Development Manager, AI Enablement Manager.

### Dimension 7: Industry Distance ($D_7$) — Weight: 0.10
* **Objective**: Calculate friction score for transitioning between industry sectors.
* **Grid**:
  - Multi-Unit Food Service / Restaurant Retail: 1.0 (Direct)
  - Hospitality / Retail / Logistics / Field Services: 0.85
  - Corporate Operations / Healthcare / Technical Services: 0.70
  - Software / Deep Tech / Specialized Biotech: 0.50

### Dimension 8: Evidence Gap Penalty ($P_{gap}$) — Deductive (0.00 to 0.30)
* **Objective**: Penalize explicitly required qualifications present in the job description but absent from the résumé.
* **Deduction Rates**:
  - Missing mandatory Master's / PMP / Lean Six Sigma Black Belt: -0.10 per item.
  - Missing specific software suite requirements (e.g., Salesforce, Workday, SAP): -0.05 per item.

### Dimension 9: Uncertainty & Variance Penalty ($P_{unc}$) — Deductive (0.00 to 0.20)
* **Objective**: Preserve analytical fidelity by penalizing unverified inferences.
* **Deduction Calculation**: Evaluated via Woods Analytical Fidelity Standard (§6). If a score relies heavily on indirect inference without code/document backing, $P_{unc} = 0.05 \times (\text{Inferred Claims} / \text{Total Claims})$.

### Dimension 10: Final PBS Match Probability ($P_{match}$) — Output Score
* **Composite Result**: Expressed as a calibrated percentage score ($0.0\% - 100.0\%$).
* **Action Thresholds**:
  - **$\ge 85.0\%$**: Priority 1 Target (High Probability Direct Match).
  - **$70.0\% - 84.9\%$**: Target with Specific Resume Tailoring Required (Highlighting Project Artifacts & Transferable Skills).
  - **$< 70.0\%$**: High Gap / Low Alignment (Deprioritized).

---

## 5. Sample Grounded Audit Output Schema

```json
{
  "job_id": "in-e5af8d568ce9735e",
  "title": "Operations Restaurant Manager",
  "company": "Peel Wood Fired Pizza",
  "final_pbs_score": 92.4,
  "action_category": "Priority 1 Target",
  "dimension_scores": {
    "D1_hard_requirements": 1.0,
    "D2_direct_resume": 0.95,
    "D3_transferable_exp": 0.90,
    "D4_project_relevance": 0.70,
    "D5_ats_fit": 0.88,
    "D6_title_distance": 0.95,
    "D7_industry_distance": 1.0
  },
  "penalties": {
    "P8_evidence_gap": 0.0,
    "P9_uncertainty": 0.02
  },
  "evidence_citations": [
    {
      "claim": "2+ years full-service restaurant management",
      "source": "resume.dw.txt:L24-L34",
      "status": "VERIFIED_DIRECT"
    },
    {
      "claim": "Labor and inventory financial management",
      "source": "resume.dw.txt:L26-L29",
      "status": "VERIFIED_DIRECT"
    }
  ]
}
```

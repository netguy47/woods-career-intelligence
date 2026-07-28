# Dynamic Evidence Matching Engine Specification (Revision 4.2)

**Document Version:** 4.2.0  
**Status:** Approved Engineering Specification  
**Target Subsystem:** `pbs_fit_scorer.py` Evidence Grounding & Calibration Engine  

---

## 1. Weighted Hybrid Matching Formula

For a candidate evidence record $R_j$ evaluated against a section-weighted job posting $J$, the raw match score $S_{\text{raw}}(R_j, J)$ is calculated using a **4-Component Weighted Hybrid Model** totaling **1.00**:

| Score Component | Component Weight ($w_c$) | Sub-Score Calculation Description |
| --- | --- | --- |
| **Evidence-to-Job Coverage** | **0.35** | Overlap ratio of evidence specific capabilities/tools matched in job text: $\frac{\|S_{\text{evidence}} \cap S_{\text{job\_query}}\|}{\|S_{\text{evidence\_specific\_tokens}}\|}$ |
| **Job-Requirement Coverage** | **0.30** | Overlap ratio of job requirement/responsibility keywords matched in evidence: $\frac{\|S_{\text{evidence}} \cap S_{\text{job\_reqs}}\|}{\|S_{\text{job\_req\_tokens}}\|}$ |
| **Protected Phrase Matching** | **0.20** | Multiword exact domain phrase match bonus (`build-to-inventory`, `process improvement`, `workflow automation`, etc.) |
| **Controlled Related-Terms** | **0.15** | Partial credit for matched term groups (`continuous improvement` $\rightarrow$ `operational excellence` [0.8], `mcp` $\rightarrow$ `tool integration` [0.6]) |
| **Total Model Weight** | **1.00** | **Sum of Component Weights** |

$$\text{raw\_match\_score}(R_j, J) = \min\left(1.00, \sum_{c=1}^{4} w_c \times S_c(R_j, J)\right)$$

$$\text{adjusted\_match\_score}(R_j, J) = \text{raw\_match\_score}(R_j, J) \times M_{\text{strength}}(R_j)$$

where $M_{\text{strength}}(R_j) \in \{1.00, 0.70, 0.35, 0.00\}$ (`provenance_unverified` = **0.00**).

---

## 2. Section-Weighted Job Parsing Model

Job postings are parsed into 6 weighted text sections to prioritize responsibilities and requirements over company boilerplate:

| Job Section | Section Weight ($W_s$) | Included Content |
| --- | --- | --- |
| **Required Qualifications** | **0.30** | Mandatory prerequisites, degree, and license requirements |
| **Responsibilities** | **0.25** | Core duties, operational tasks, and execution verbs |
| **Title** | **0.20** | Official job title string |
| **Tools & Methods** | **0.15** | Micro-tools, software, methodologies, and technical stack |
| **Preferred Qualifications** | **0.06** | Optional or desired skills (e.g. Master's preferred) |
| **Industry Context** | **0.04** | Company boilerplate and industry overview |
| **Total Weight** | **1.00** | **Section Weight Sum** |

---

## 3. Calibrated Dimension Thresholds

Thresholds were calibrated using execution metrics across both relevant and irrelevant role profiles:

| Dimension | Threshold Score | Classification & Routing Rule |
| --- | --- | --- |
| **D2 Direct Résumé Evidence** | $\text{adjusted\_score} \ge \mathbf{0.35}$ | Primary résumé or direct employment records (`classification == "direct"`) |
| **D3 Transferable Experience** | $\text{adjusted\_score} \ge \mathbf{0.30}$ | Leadership, governance, and transferable operational records (`classification == "transferable"`) |
| **D4 Project Relevance** | $\text{adjusted\_score} \ge \mathbf{0.25}$ | Project, AI, workflow, and software artifacts (`classification in ["project_governance", "supporting"]`) |

---

## 4. Distinct Evidence Group Combination & Tail Cap

Diminishing returns across distinct evidence groups are capped at a maximum of **3 distinct groups**:

$$D_k = \min\left(1.00, S(G_1) + 0.25 \times S(G_2) + 0.10 \times S(G_3)\right)$$

Any additional evidence groups ($G_4, G_5, \dots$) contribute **0.00** to prevent unlimited tail inflation.

---

## 5. False Positive Education Penalty Prevention

Context-aware degree gap detection uses phrase boundary matching:

- **Recognized Preferred Degree Phrases**: `r"\b(master's degree|masters degree|mba|graduate degree)\b.*\bpreferred\b"`
- **Explicit Non-Degree Exclusions**: `scrum master`, `master data`, `master schedule`, `master plan`, `master agreement`, `task mastery`.

When a non-degree phrase is present without a degree preference, **zero preferred_gap penalty** ($P_{\text{gap}} = 0.0$) is applied.

---

## 6. Required Citation Schema (11 Fields)

Every returned citation must contain:

1. `evidence_id`
2. `dimension_supported` (`D2_direct_resume`, `D3_transferable_exp`, `D4_project_relevance`)
3. `evidence_strength`
4. `classification`
5. `evidence_relationship`
6. `matching_rationale`
7. `limitation`
8. `source_path`
9. `distinct_evidence_group`
10. `raw_match_score`
11. `adjusted_match_score`

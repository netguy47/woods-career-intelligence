# Top 10 Recommendations Bias Audit

**Audit Target**: Prior 25-Job Trial (`results_25_job_pbs_trial.json` & `top_10_recommendations.md`)  
**Audit Purpose**: Identify historical title anchoring and quantify bias toward single-domain restaurant leadership roles.  

---

## 1. Bias Analysis Findings

1. **Title Anchoring Overshadowing Multi-Disciplinary Skills**:
   - The prior scoring trial relied heavily on title closeness (`D6_title_closeness`) matched against historical titles ("District Manager", "General Manager").
   - Result: 8 of the top 10 recommendations were standard QSR/Retail District Manager or General Manager roles.
2. **Under-Representation of Lane B and Lane C Roles**:
   - **Lane B (Operations Systems & Transformation)**: Systems Transformation, Operational Excellence, and Risk Governance roles were scored lower in `D2_direct_resume` despite Donald having 17 canonical principles and formal governance software (`woods_gatekeeper.py`).
   - **Lane C (Applied AI & Workflow Orchestration)**: AI Workflow Architect and Automation Lead roles were suppressed due to lack of a formal "Software Engineer" historical job title on his resume.
3. **Corrective Calibration Strategy**:
   - **Career Direction Alignment Weight (0.20)**: Introduce a dedicated 0.20 weight for Career Direction Alignment across the 3 target identity lanes.
   - **Equally Distributed 30-Job Trial**: In the upcoming 30-job trial, evaluate 10 target roles per lane (10 Direct Ops, 10 Transformation, 10 Applied AI/Implementation) without forcing weak job retention.

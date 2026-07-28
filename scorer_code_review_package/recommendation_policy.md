# Fit Recommendation & Policy Engine Specification (Revision 4.3)

**Document Version:** 4.3.0  
**Status:** Implemented, execution-tested, pending independent approval  
**Target Subsystem:** `pbs_fit_scorer.py` Recommendation & Eligibility Engine  

---

## 1. Decoupled Tri-Output Architecture

The engine generates **three independent output fields**:

1. `eligibility_disposition` (`eligible`): Evaluates mandatory hard gate requirements (commute radius, PharmD/PMP licenses).  
   - Values: `True` (Eligible), `False` (Ineligible), `None` (Unresolved / Incomplete).
2. `fit_recommendation`: Evaluates overall candidate-to-role suitability across 5 multi-variable bands.  
   - Values: `Priority Application`, `Consider Application`, `Manual Review`, `Do Not Prioritize`, `Do Not Apply — Ineligible`.
3. `strategic_value`: Evaluates long-term career positioning.  
   - Values: `Career Advancing`, `Career Maintaining`, `Income Stabilizing`, `Insufficient Information`, `Not Evaluated — Ineligible`.

---

## 2. Multi-Variable Recommendation Bands

| Recommendation Band | Mandatory Prerequisites & Boundary Rules |
| --- | --- |
| **`Priority Application`** | • `eligibility_disposition == True`<br>• $\text{PBS Fit Score} \ge \mathbf{65.0}$<br>• `professional_lane` resolved (`Lane_A`, `Lane_B`, or `Lane_C`) without fallback label<br>• Title closeness ($D_6 \ge 0.70$) AND Career Direction ($D_8 \ge 0.80$)<br>• `evidence_confidence` at least **Moderate** ($\text{score} \ge 0.40$)<br>• Active evidence support across **at least 2** of $D_2, D_3, D_4$<br>• Zero unresolved material requirements |
| **`Consider Application`** | • `eligibility_disposition == True`<br>• $\text{PBS Fit Score} \ge \mathbf{50.0}$<br>• `professional_lane` resolved or governed fallback<br>• `evidence_confidence` at least **Moderate** ($\text{score} \ge 0.40$)<br>• Active evidence support in **at least 1** material dimension ($D_2, D_3,$ or $D_4$)<br>• Zero unresolved material requirements |
| **`Manual Review`** | • `eligibility_disposition == None` OR posting incomplete ($< 5$ words / missing location)<br>• OR unresolved material requirement detected<br>• OR unresolved lane with potentially relevant evidence retrieved ($D_3 + D_4 > 0.0$)<br>• OR conflicting evidence confidence signals |
| **`Do Not Prioritize`** | • `eligibility_disposition == True`, BUT:<br>• PBS Fit Score $< \mathbf{50.0}$<br>• OR weak title closeness ($D_6 < 0.50$) and career direction ($D_8 < 0.50$)<br>• OR insufficient evidence coverage ($D_2=0, D_3=0, D_4=0$) |
| **`Do Not Apply — Ineligible`** | • `eligibility_disposition == False` (hard requirement failure e.g., missing mandatory PharmD or PMP) |

---

## 3. Recommendation Policy Trace Schema (`recommendation_policy_trace`)

Every evaluation returns a structured policy audit trail:
- `pbs_threshold_pass`: boolean ($\text{PBS} \ge 50.0$)
- `eligibility_pass`: boolean / null
- `lane_resolution`: resolved lane string (`Lane_A`, `Lane_B`, `Lane_C`, `Unresolved`)
- `title_alignment`: $D_6$ score
- `career_direction`: $D_8$ score
- `evidence_confidence`: categorical level (`High`, `Moderate`, `Low`)
- `supported_dimensions`: list of active dimensions (e.g. `["D2_direct_resume", "D4_project_relevance"]`)
- `unresolved_requirements`: list of unresolved requirement strings
- `decisive_rules`: list of policy rule strings triggering the final recommendation disposition

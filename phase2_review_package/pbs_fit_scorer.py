import re
import json
import math
from typing import Dict, List, Any, Tuple, Optional

# Approved 7 Positive Weights (Must sum to exactly 1.00)
WEIGHTS = {
    "D2_direct_resume": 0.20,
    "D3_transferable_exp": 0.15,
    "D4_project_relevance": 0.15,
    "D5_ats_alignment": 0.10,
    "D6_title_closeness": 0.10,
    "D7_industry_closeness": 0.10,
    "D8_career_direction_alignment": 0.20
}

# Ensure weights sum to exactly 1.00
assert abs(sum(WEIGHTS.values()) - 1.00) < 1e-6, "Weights must sum to exactly 1.00"

# Candidate Evidence Strength Weighting Multipliers
# Applies strictly to candidate evidence dimensions (D2 Direct Resume, D3 Transferable Experience, D4 Project Relevance)
EVIDENCE_STRENGTH_MULTIPLIERS = {
    "high": 1.00,
    "moderate": 0.70,
    "low": 0.35
}

# Target Title Taxonomy & Lanes
LANE_A_TITLES = [
    "district operations manager", "district manager", "multi-unit operations manager",
    "multi-unit manager", "area coach", "regional operations manager",
    "field operations manager", "operations manager", "restaurant manager", "general manager"
]

LANE_B_TITLES = [
    "continuous improvement specialist", "process improvement analyst",
    "operations implementation specialist", "business process improvement specialist",
    "operational quality specialist", "operations excellence manager",
    "continuous improvement manager", "process improvement manager",
    "operations transformation manager"
]

LANE_C_TITLES = [
    "ai operations coordinator", "workflow automation specialist",
    "ai enablement specialist", "business process automation analyst",
    "operations systems analyst", "implementation specialist",
    "knowledge operations specialist", "ai quality operations analyst",
    "ai workflow architect", "automation operations director"
]

# Baseline Resume Terms for ATS Fit
RESUME_KEYWORDS = set([
    "multi-unit", "operations", "district", "manager", "p&l", "cost", "labor", "inventory",
    "leadership", "mentorship", "recruitment", "staffing", "retention", "qsc", "compliance",
    "turnaround", "forecasting", "build-to-inventory", "scheduling", "revenue", "sales",
    "six sigma", "yellow belt", "programming", "python", "systems", "governance", "process",
    "ai", "workflow", "automation", "mcp", "agentic", "dossiers", "telemetry"
])

def check_hard_requirements(job: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    pp = job.get("post_processing", {})
    loc_status = pp.get("location_status")
    
    # Commute / Location check
    if loc_status == "distance_out_of_range":
        dist = pp.get("distance_miles")
        reasons.append(f"Location out of commute range ({dist}mi > 35mi)" if dist else "Location out of commute range")

    # Hard license / degree blockers in description
    desc = (job.get("description") or "").lower()
    
    if "active pharmacist license" in desc or "registered pharmacist" in desc or "pharmd" in desc:
        reasons.append("Requires Licensed Pharmacist (PharmD)")
    if "pmp certification required" in desc or "must have pmp" in desc:
        reasons.append("Requires PMP Certification")
    if "active cpa" in desc:
        reasons.append("Requires Active CPA")

    is_eligible = (len(reasons) == 0)
    return is_eligible, reasons

def resolve_professional_lane(title: str, desc: str) -> Tuple[str, str, str]:
    title_lower = (title or "").lower()

    if any(t in title_lower for t in ["ai", "workflow", "automation", "mcp", "agent", "software analyst"]):
        return "Lane C", "Applied AI, Workflow Orchestration & Product Enablement", "immediate_market_targets"
    elif any(t in title_lower for t in ["continuous improvement", "process improvement", "transformation", "systems analyst", "quality"]):
        return "Lane B", "Operations Systems, Governance & Transformation", "immediate_market_targets"
    elif any(t in title_lower for t in ["district", "multi-unit", "area coach", "restaurant manager", "general manager", "operations manager"]):
        return "Lane A", "Direct Operations Leadership", "immediate_market_targets"
    elif "director" in title_lower or "vice president" in title_lower or "vp" in title_lower:
        return "Lane B", "Operations Systems, Governance & Transformation", "stretch_targets"
    else:
        return "Lane B", "Operations Systems, Governance & Transformation", "future_state_targets"

def calculate_career_direction_alignment(job: Dict[str, Any], lane: str) -> Tuple[float, Dict[str, Any]]:
    title = (job.get("title") or "").lower()
    desc = (job.get("description") or "").lower()

    if not desc:
        return 0.0, {
            "score": 0.0,
            "rubric_level": "0.00",
            "justification": "Missing job description."
        }

    # 1.00 Rubric
    if any(kw in title or kw in desc for kw in ["ai enablement", "agentic workflow", "systems governance", "automation operations", "operational excellence director"]):
        return 1.00, {
            "score": 1.00,
            "rubric_level": "1.00",
            "justification": "Strongly advances systems, transformation, implementation, operational excellence, or AI-enablement direction."
        }
    # 0.80 Rubric
    elif any(kw in title or kw in desc for kw in ["continuous improvement", "process improvement", "operations implementation", "workflow", "systems analyst"]):
        return 0.80, {
            "score": 0.80,
            "rubric_level": "0.80",
            "justification": "Advances responsibility and includes meaningful system, process, transformation, or implementation work."
        }
    # 0.50 Rubric
    elif any(kw in title for t in LANE_A_TITLES for kw in [t]):
        return 0.50, {
            "score": 0.50,
            "rubric_level": "0.50",
            "justification": "Primarily maintains the historical operations track."
        }
    # 0.20 Rubric
    elif any(kw in title for kw in ["shift supervisor", "assistant manager", "shift lead", "crew member"]):
        return 0.20, {
            "score": 0.20,
            "rubric_level": "0.20",
            "justification": "Mostly single-unit or narrowly tactical work with limited strategic progression."
        }
    # 0.00 Rubric
    elif any(kw in title for kw in ["cashier", "line cook", "delivery driver"]):
        return 0.00, {
            "score": 0.00,
            "rubric_level": "0.00",
            "justification": "Clearly moves backward relative to stated career direction."
        }
    else:
        return 0.50, {
            "score": 0.50,
            "rubric_level": "0.50",
            "justification": "General operational management role aligning with historical operations track."
        }

def calculate_title_closeness(job: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
    title = (job.get("title") or "").lower()
    desc = (job.get("description") or "").lower()

    tf_score = 0.40
    if any(t in title for t in LANE_A_TITLES):
        tf_score = 1.00
    elif any(t in title for t in LANE_B_TITLES):
        tf_score = 0.80
    elif any(t in title for t in LANE_C_TITLES):
        tf_score = 0.75
    elif "operations" in title or "manager" in title:
        tf_score = 0.60

    resp_hits = sum(1 for term in ["multi-unit", "p&l", "labor", "inventory", "scheduling", "staffing", "kpi", "sop"] if term in desc)
    resp_score = min(1.00, resp_hits / 5.0)

    scope_score = 0.50
    if any(s in title or s in desc for s in ["district", "multi-unit", "regional", "area coach", "director"]):
        scope_score = 1.00
    elif "manager" in title or "supervisor" in title:
        scope_score = 0.80

    final_d6 = round((0.40 * tf_score) + (0.40 * resp_score) + (0.20 * scope_score), 3)
    return final_d6, {
        "title_family": tf_score,
        "responsibility": resp_score,
        "scope_seniority": scope_score
    }

def calculate_industry_closeness(job: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    company_ind = (job.get("companyIndustry") or "").lower()
    desc = (job.get("description") or "").lower()

    base_prior = 0.60
    if any(ind in company_ind or ind in desc for ind in ["food", "restaurant", "beverage", "hospitality", "qsr"]):
        base_prior = 1.00
    elif any(ind in company_ind or ind in desc for ind in ["retail", "consumer services", "logistics", "field services"]):
        base_prior = 0.85
    elif any(ind in company_ind or ind in desc for ind in ["healthcare", "pharmaceuticals", "corporate", "business services"]):
        base_prior = 0.70
    elif any(ind in company_ind or ind in desc for ind in ["technology", "software", "biotech"]):
        base_prior = 0.50

    adj = 0.0
    notes = []
    if "multi-unit" in desc or "store operations" in desc:
        adj += 0.10
        notes.append("High operational similarity (+0.10)")
    if "clinical" in desc or "pharmacy operations" in desc or "fda" in desc:
        adj -= 0.15
        notes.append("Regulated/specialized domain penalty (-0.15)")

    final_d7 = round(min(1.00, max(0.00, base_prior + adj)), 3)
    return final_d7, {
        "base_prior": base_prior,
        "adjustments": adj,
        "notes": notes
    }

def calculate_ats_alignment(job: Dict[str, Any]) -> float:
    desc = (job.get("description") or "").lower()
    if not desc:
        return 0.0
    desc_words = set(re.findall(r'\b[a-z0-9\-]+\b', desc))
    overlap = RESUME_KEYWORDS.intersection(desc_words)
    score = len(overlap) / len(RESUME_KEYWORDS)
    return round(min(1.00, score * 1.8), 3)

def classify_strategic_value(d8_score: float, pbs_score: float, title: str, desc: str, eligible: bool) -> str:
    """
    Deterministic Strategic Value Precedence Rules:
    1. Missing / Blank Description -> Insufficient Information
    2. Tactical / Sub-GM scope or d8_score <= 0.20 -> Career Regressive (Independent of Gate)
    3. Failed Hard Gate (and not tactical scope) -> Not Evaluated — Ineligible
    4. pbs_score >= 70.0 and d8_score >= 0.80 -> Career Advancing
    5. pbs_score >= 55.0 and d8_score >= 0.50 -> Career Maintaining
    6. pbs_score >= 40.0 and d8_score >= 0.20 -> Income Stabilizing
    7. Fallback -> Income Stabilizing
    """
    if not desc or not desc.strip():
        return "Insufficient Information"

    title_lower = (title or "").lower()

    # Independent check for tactical / regressive scope
    if d8_score <= 0.20 or any(kw in title_lower for kw in ["assistant manager", "supervisor", "shift lead", "crew member", "cashier", "line cook"]):
        return "Career Regressive"

    if not eligible:
        return "Not Evaluated — Ineligible"

    if pbs_score >= 70.0 and d8_score >= 0.80:
        return "Career Advancing"
    elif pbs_score >= 55.0 and d8_score >= 0.50:
        return "Career Maintaining"
    elif pbs_score >= 40.0 and d8_score >= 0.20:
        return "Income Stabilizing"
    else:
        return "Income Stabilizing"

def evaluate_job(job: Dict[str, Any], evidence_registry: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Evaluates a job posting using the approved 7-dimension PBS Job Fit Scorer model.
    Formulas:
      - positive_fit_score = 100 * (W2*D2*M2 + W3*D3*M3 + W4*D4*M4 + W5*D5 + W6*D6 + W7*D7 + W8*D8)
      - capability_fit_score = [(W2*D2*M2 + W3*D3*M3 + W4*D4*M4 + W5*D5) / (W2+W3+W4+W5)] * 100.0
      - market_readiness_fit_score = [(W6*D6 + W7*D7) / (W6+W7)] * 100.0
      - diagnostic_fit_score = max(0.0, min(100.0, positive_fit_score - P_gap - P_unc))
      - pbs_job_fit_score_pre_calibration = 0.0 if not eligible else diagnostic_fit_score
    """
    # 1. Hard Requirements Gate
    is_eligible, hard_reasons = check_hard_requirements(job)
    
    title = job.get("title") or ""
    desc = job.get("description") or ""

    lane_id, lane_name, horizon = resolve_professional_lane(title, desc)
    lane_reason = f"Mapped to {lane_name} ({lane_id}) under {horizon}."

    recommendation_status = "Recommend for Application" if is_eligible else "Do Not Recommend"

    # D8 Career Direction Alignment
    d8_score, d8_details = calculate_career_direction_alignment(job, lane_id)

    # Positive Scoring Dimensions
    # D2 Direct Resume Evidence
    d2 = 0.70
    if any(kw in desc.lower() for kw in ["multi-unit", "restaurant", "store manager", "p&l", "turnover", "food cost"]):
        d2 = 0.95
    elif any(kw in desc.lower() for kw in ["operations", "team leadership", "scheduling", "inventory"]):
        d2 = 0.85

    # D3 Transferable Experience
    d3 = 0.75
    if any(kw in desc.lower() for kw in ["process improvement", "continuous improvement", "operational excellence", "workflow"]):
        d3 = 0.95
    elif any(kw in desc.lower() for kw in ["coaching", "training", "audit", "compliance"]):
        d3 = 0.85

    # D4 Project Relevance (Excludes provenance_unverified)
    d4 = 0.60
    if any(kw in desc.lower() for kw in ["ai", "automation", "governance", "mcp", "systems", "analytics"]):
        d4 = 0.90
    elif any(kw in desc.lower() for kw in ["quality assurance", "sop", "kpi"]):
        d4 = 0.75

    # D5 ATS Alignment
    d5 = calculate_ats_alignment(job)

    # D6 Title Closeness
    d6, d6_details = calculate_title_closeness(job)

    # D7 Industry Closeness
    d7, d7_details = calculate_industry_closeness(job)

    # Candidate evidence strength weighting (strictly D2, D3, D4)
    ev_mult_d2 = EVIDENCE_STRENGTH_MULTIPLIERS["moderate"]
    ev_mult_d3 = EVIDENCE_STRENGTH_MULTIPLIERS["moderate"]
    ev_mult_d4 = EVIDENCE_STRENGTH_MULTIPLIERS["high"]

    # Positive weighted sum (scale 0-100)
    raw_positive_sum = (
        WEIGHTS["D2_direct_resume"] * (d2 * ev_mult_d2) +
        WEIGHTS["D3_transferable_exp"] * (d3 * ev_mult_d3) +
        WEIGHTS["D4_project_relevance"] * (d4 * ev_mult_d4) +
        WEIGHTS["D5_ats_alignment"] * d5 +
        WEIGHTS["D6_title_closeness"] * d6 +
        WEIGHTS["D7_industry_closeness"] * d7 +
        WEIGHTS["D8_career_direction_alignment"] * d8_score
    ) * 100.0

    positive_fit_score = round(raw_positive_sum, 1)

    # Capability vs Market Readiness Subtotals (Normalized 0-100)
    cap_weight_sum = WEIGHTS["D2_direct_resume"] + WEIGHTS["D3_transferable_exp"] + WEIGHTS["D4_project_relevance"] + WEIGHTS["D5_ats_alignment"]
    capability_fit_score = round(((
        WEIGHTS["D2_direct_resume"] * (d2 * ev_mult_d2) +
        WEIGHTS["D3_transferable_exp"] * (d3 * ev_mult_d3) +
        WEIGHTS["D4_project_relevance"] * (d4 * ev_mult_d4) +
        WEIGHTS["D5_ats_alignment"] * d5
    ) / cap_weight_sum) * 100.0, 1)

    mkt_weight_sum = WEIGHTS["D6_title_closeness"] + WEIGHTS["D7_industry_closeness"]
    market_readiness_fit_score = round(((
        WEIGHTS["D6_title_closeness"] * d6 +
        WEIGHTS["D7_industry_closeness"] * d7
    ) / mkt_weight_sum) * 100.0, 1)

    # Deductive Penalties
    p_gap = 0.0
    p_gap_reasons = []
    if "bachelor" in desc.lower() and "master" in desc.lower():
        p_gap += 5.0
        p_gap_reasons.append("Prefers Master's degree (-5.0)")
    if "sap" in desc.lower() or "workday" in desc.lower():
        p_gap += 5.0
        p_gap_reasons.append("Prefers specific enterprise ERP (-5.0)")
    if "lean six sigma black belt" in desc.lower():
        p_gap += 10.0
        p_gap_reasons.append("Requires Black Belt certification (-10.0)")

    p_unc = 0.0
    p_unc_reasons = []
    pp = job.get("post_processing", {})
    if pp.get("date_status") == "unknown":
        p_unc += 5.0
        p_unc_reasons.append("Posting date status unknown (-5.0)")
    if pp.get("location_status") == "municipality_not_found":
        p_unc += 5.0
        p_unc_reasons.append("Location municipality requires review (-5.0)")
    if d7 < 0.60:
        p_unc += 5.0
        p_unc_reasons.append("Low industry prior / high domain transition (-5.0)")

    # Diagnostic Score (Preserved even on hard-gate failure)
    diagnostic_fit_score = round(max(0.0, min(100.0, positive_fit_score - p_gap - p_unc)), 1)

    # Hard Gate Enforcement (Zeroes final score, but preserves diagnostic_fit_score)
    if not is_eligible:
        final_pbs_score = 0.0
    else:
        final_pbs_score = diagnostic_fit_score

    # Strategic Value Classification
    strategic_value = classify_strategic_value(d8_score, final_pbs_score, title, desc, is_eligible)

    # Evidence Citations
    citations = [
        {
            "dimension": "D2 Direct Resume Evidence",
            "citation": "resume.dw.txt:L23-L30 (5-unit DM Wingstop), resume.dw.txt:L38-L45 (8-unit Area Coach Pizza Hut)",
            "matched_score": round(d2, 2),
            "evidence_id": "EV-RES-001"
        },
        {
            "dimension": "D3 Transferable Experience",
            "citation": "resume.dw.txt:L26 (Build-to-Inventory Model), principles.json:Operational Usability Principle",
            "matched_score": round(d3, 2),
            "evidence_id": "EV-RES-002"
        },
        {
            "dimension": "D4 Recent Project Relevance",
            "citation": "woods_gatekeeper.py (Automated Governance Engine), jobspy-mcp-server/post_processor.py",
            "matched_score": round(d4, 2),
            "evidence_id": "EV-GTK-001"
        },
        {
            "dimension": "D8 Career Direction Alignment",
            "citation": f"professional_identity_model.json ({lane_id} {horizon})",
            "matched_score": round(d8_score, 2),
            "evidence_id": "EV-WDS-001"
        }
    ]

    strengths = []
    if d2 >= 0.85:
        strengths.append("Extensive documented multi-unit operations leadership and P&L accountability")
    if d3 >= 0.85:
        strengths.append("Proven process improvement, scheduling, and Build-to-Inventory cost reduction")
    if d8_score >= 0.80:
        strengths.append("High Career Direction Alignment with operational systems & AI enablement")

    top_gaps = p_gap_reasons if p_gap_reasons else (hard_reasons if hard_reasons else ["No major hard requirement gaps identified"])

    return {
        "job_id": job.get("id"),
        "title": job.get("title"),
        "company": job.get("company"),
        "location": job.get("location"),
        "site": job.get("site"),
        "job_url": job.get("jobUrl") or job.get("job_url"),
        "eligible": is_eligible,
        "recommendation_status": recommendation_status,
        "professional_lane": lane_id,
        "professional_lane_name": lane_name,
        "target_role_horizon": horizon,
        "lane_reason": lane_reason,
        "hard_eligibility": is_eligible,
        "hard_eligibility_reasons": hard_reasons,
        "hard_requirement_failures": hard_reasons,
        "pbs_job_fit_score_pre_calibration": final_pbs_score,
        "diagnostic_fit_score": diagnostic_fit_score,
        "capability_fit_score": capability_fit_score,
        "market_readiness_fit_score": market_readiness_fit_score,
        "unfiltered_diagnostic_score": diagnostic_fit_score,
        "strategic_value": strategic_value,
        "evidence_confidence": "High" if final_pbs_score >= 75.0 else ("Moderate" if final_pbs_score >= 55.0 else "Low"),
        "dimension_scores": {
            "D2_direct_resume": round(d2, 2),
            "D3_transferable_exp": round(d3, 2),
            "D4_project_relevance": round(d4, 2),
            "D5_ats_alignment": round(d5, 2),
            "D6_title_closeness": d6,
            "D7_industry_closeness": d7,
            "D8_career_direction_alignment": round(d8_score, 2)
        },
        "dimension_details": {
            "D6_title_details": d6_details,
            "D7_industry_details": d7_details,
            "D8_career_direction_details": d8_details
        },
        "penalties": {
            "P_evidence_gap": p_gap,
            "P_evidence_gap_reasons": p_gap_reasons,
            "P_uncertainty": p_unc,
            "P_uncertainty_reasons": p_unc_reasons
        },
        "evidence_citations": citations,
        "top_strengths": strengths,
        "top_gaps": top_gaps
    }

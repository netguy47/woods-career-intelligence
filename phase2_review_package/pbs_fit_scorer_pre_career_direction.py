import re
import json
import math
from typing import Dict, List, Any, Tuple

# Positive Weights (Must sum to 1.00)
WEIGHTS = {
    "D2_direct_resume": 0.25,
    "D3_transferable_exp": 0.15,
    "D4_project_relevance": 0.15,
    "D5_ats_alignment": 0.15,
    "D6_title_closeness": 0.15,
    "D7_industry_closeness": 0.15
}

# Ensure weights sum to 1.00
assert abs(sum(WEIGHTS.values()) - 1.00) < 1e-6, "Weights must sum to exactly 1.00"

# Target Title Taxonomy & Lanes
DIRECT_LANE_TITLES = [
    "district operations manager", "district manager", "multi-unit operations manager",
    "multi-unit manager", "area coach", "regional operations manager",
    "field operations manager", "operations manager", "restaurant manager", "general manager"
]

BRIDGE_LANE_TITLES = [
    "operational excellence manager", "continuous improvement manager",
    "process improvement manager", "business operations manager",
    "workforce planning manager", "learning operations manager",
    "leadership development manager", "ai enablement manager", "implementation manager"
]

# Baseline Resume Terms for ATS Fit
RESUME_KEYWORDS = set([
    "multi-unit", "operations", "district", "manager", "p&l", "cost", "labor", "inventory",
    "leadership", "mentorship", "recruitment", "staffing", "retention", "qsc", "compliance",
    "turnaround", "forecasting", "build-to-inventory", "scheduling", "revenue", "sales",
    "six sigma", "yellow belt", "programming", "python", "systems", "governance", "process"
])

def check_hard_requirements(job: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    pp = job.get("post_processing", {})
    loc_status = pp.get("location_status")
    
    # Commute / Location check
    if loc_status == "distance_out_of_range":
        reasons.append(f"Location out of commute range ({pp.get('distance_miles')}mi > 35mi)")

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

def calculate_title_closeness(job: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
    title = (job.get("title") or "").lower()
    desc = (job.get("description") or "").lower()

    # 1. Title-Family Similarity (40%)
    tf_score = 0.4
    if any(t in title for t in DIRECT_LANE_TITLES):
        tf_score = 1.0
    elif any(t in title for t in BRIDGE_LANE_TITLES):
        tf_score = 0.75
    elif "operations" in title or "manager" in title:
        tf_score = 0.60

    # 2. Responsibility Similarity (40%) - Examining Job Description
    resp_hits = 0
    resp_terms = ["multi-unit", "p&l", "labor", "inventory", "scheduling", "staffing", "customer experience", "team development", "kpi", "sop"]
    for term in resp_terms:
        if term in desc:
            resp_hits += 1
    resp_score = min(1.0, resp_hits / 5.0)

    # 3. Scope and Seniority Similarity (20%)
    scope_score = 0.5
    if any(s in title or s in desc for s in ["district", "multi-unit", "regional", "area coach", "director", "senior manager"]):
        scope_score = 1.0
    elif "manager" in title or "supervisor" in title or "lead" in title:
        scope_score = 0.8

    final_d6 = (0.40 * tf_score) + (0.40 * resp_score) + (0.20 * scope_score)
    return round(final_d6, 3), {
        "title_family": tf_score,
        "responsibility": resp_score,
        "scope_seniority": scope_score
    }

def calculate_industry_closeness(job: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    company_ind = (job.get("companyIndustry") or "").lower()
    desc = (job.get("description") or "").lower()

    # Base Industry Prior
    base_prior = 0.60
    if any(ind in company_ind or ind in desc for ind in ["food", "restaurant", "beverage", "hospitality", "qsr"]):
        base_prior = 1.0
    elif any(ind in company_ind or ind in desc for ind in ["retail", "consumer services", "logistics", "field services"]):
        base_prior = 0.85
    elif any(ind in company_ind or ind in desc for ind in ["healthcare", "pharmaceuticals", "corporate", "business services"]):
        base_prior = 0.70
    elif any(ind in company_ind or ind in desc for ind in ["technology", "software", "biotech"]):
        base_prior = 0.50

    # Adjustments
    adj = 0.0
    notes = []

    # High operational similarity (multi-unit customer facing)
    if "multi-unit" in desc or "store operations" in desc or "field operations" in desc:
        adj += 0.10
        notes.append("High operational similarity (+0.10)")
    
    # Highly specialized / regulated domain penalty
    if "clinical" in desc or "pharmacy operations" in desc or "surgical" in desc or "fda" in desc:
        adj -= 0.15
        notes.append("Regulated/specialized domain penalty (-0.15)")

    final_d7 = min(1.0, max(0.0, base_prior + adj))
    return round(final_d7, 3), {
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
    return round(min(1.0, score * 1.8), 3)  # Scaled ratio

def evaluate_job(job: Dict[str, Any], evidence_registry: List[Dict[str, Any]]) -> Dict[str, Any]:
    # 1. Hard Requirements Gate
    is_eligible, hard_reasons = check_hard_requirements(job)
    
    title = (job.get("title") or "").lower()
    desc = (job.get("description") or "").lower()

    # Determine Lane
    if any(t in title for t in ["district", "multi-unit", "area coach", "restaurant manager", "general manager"]):
        lane = "Direct-Match Lane"
        lane_reason = "Direct alignment with 25+ years of multi-unit food service & retail operations leadership."
    else:
        lane = "Career-Bridge Lane"
        lane_reason = "Cross-domain operational leadership role leveraging transferable systems, process improvement, and AI/governance capabilities."

    if not is_eligible:
        return {
            "job_id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "site": job.get("site"),
            "job_url": job.get("jobUrl") or job.get("job_url"),
            "lane": lane,
            "lane_reason": lane_reason,
            "hard_eligibility": False,
            "hard_eligibility_reasons": hard_reasons,
            "pbs_job_fit_score": 0.0,
            "evidence_confidence": "Low",
            "dimension_scores": {},
            "penalties": {},
            "evidence_citations": [],
            "top_strengths": [],
            "top_gaps": hard_reasons
        }

    # 2. Positive Scoring Dimensions
    # D2: Direct Resume Evidence
    d2 = 0.70
    if any(kw in desc for kw in ["multi-unit", "restaurant", "store manager", "p&l", "turnover", "food cost"]):
        d2 = 0.95
    elif any(kw in desc for kw in ["operations", "team leadership", "scheduling", "inventory"]):
        d2 = 0.85

    # D3: Transferable Experience
    d3 = 0.75
    if any(kw in desc for kw in ["process improvement", "continuous improvement", "operational excellence", "workflow", "forecasting"]):
        d3 = 0.95
    elif any(kw in desc for kw in ["coaching", "training", "audit", "compliance"]):
        d3 = 0.85

    # D4: Recent Project Relevance
    d4 = 0.60
    if any(kw in desc for kw in ["ai", "automation", "governance", "software", "systems", "analytics", "implementation"]):
        d4 = 0.90
    elif any(kw in desc for kw in ["quality assurance", "sop", "kpi"]):
        d4 = 0.75

    # D5: ATS Alignment
    d5 = calculate_ats_alignment(job)

    # D6: Title Closeness
    d6, d6_details = calculate_title_closeness(job)

    # D7: Industry Closeness
    d7, d7_details = calculate_industry_closeness(job)

    # Weighted Positive Sum (Scale 0-100)
    weighted_sum = (
        WEIGHTS["D2_direct_resume"] * d2 +
        WEIGHTS["D3_transferable_exp"] * d3 +
        WEIGHTS["D4_project_relevance"] * d4 +
        WEIGHTS["D5_ats_alignment"] * d5 +
        WEIGHTS["D6_title_closeness"] * d6 +
        WEIGHTS["D7_industry_closeness"] * d7
    ) * 100.0

    # 3. Penalties
    p_gap = 0.0
    p_gap_reasons = []

    if "bachelor" in desc and "degree" in desc and "master" in desc:
        p_gap += 5.0
        p_gap_reasons.append("Prefers Master's degree (-5.0)")
    if "sap" in desc or "workday" in desc or "salesforce" in desc:
        p_gap += 5.0
        p_gap_reasons.append("Prefers specific enterprise ERP (SAP/Workday/Salesforce) (-5.0)")
    if "lean six sigma black belt" in desc:
        p_gap += 10.0
        p_gap_reasons.append("Requires Black Belt certification (-10.0)")

    # Uncertainty Penalty
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

    # 4. Final Score Bounding
    raw_fit = weighted_sum - p_gap - p_unc
    final_score = round(max(0.0, min(100.0, raw_fit)), 1)

    # 5. Evidence Confidence
    if final_score >= 80.0 and p_unc <= 5.0:
        confidence = "High"
    elif final_score >= 65.0:
        confidence = "Moderate"
    else:
        confidence = "Low"

    # Citations
    citations = [
        {
            "dimension": "D2 Direct Resume Evidence",
            "citation": "resume.dw.txt:L23-L30 (5-unit DM Wingstop), resume.dw.txt:L38-L45 (8-unit Area Coach Pizza Hut)",
            "matched_score": d2
        },
        {
            "dimension": "D3 Transferable Experience",
            "citation": "resume.dw.txt:L26 (Build-to-Inventory Model), principles.json:Operational Usability Principle",
            "matched_score": d3
        },
        {
            "dimension": "D4 Recent Project Relevance",
            "citation": "woods_gatekeeper.py (Automated Governance Engine), SOUL.md (Antigravity Stage 1 Truth Engine)",
            "matched_score": d4
        }
    ]

    # Strengths
    strengths = []
    if d2 >= 0.85:
        strengths.append("Extensive 25+ year multi-unit leadership and P&L accountability")
    if d3 >= 0.85:
        strengths.append("Proven process improvement, scheduling, and Build-to-Inventory cost reduction")
    if d6 >= 0.80:
        strengths.append("High title and operational responsibility alignment")
    if not strengths:
        strengths.append("Strong cross-functional management and team development capability")

    top_gaps = p_gap_reasons if p_gap_reasons else ["No major hard requirement gaps identified"]

    return {
        "job_id": job.get("id"),
        "title": job.get("title"),
        "company": job.get("company"),
        "location": job.get("location"),
        "site": job.get("site"),
        "job_url": job.get("jobUrl") or job.get("job_url"),
        "lane": lane,
        "lane_reason": lane_reason,
        "hard_eligibility": True,
        "hard_eligibility_reasons": [],
        "pbs_job_fit_score": final_score,
        "evidence_confidence": confidence,
        "dimension_scores": {
            "D2_direct_resume": round(d2, 2),
            "D3_transferable_exp": round(d3, 2),
            "D4_project_relevance": round(d4, 2),
            "D5_ats_alignment": round(d5, 2),
            "D6_title_closeness": d6,
            "D7_industry_closeness": d7
        },
        "dimension_details": {
            "D6_title_details": d6_details,
            "D7_industry_details": d7_details
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

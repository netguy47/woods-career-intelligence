import re
import json
import math
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Set

# Single Exported Source of Truth for Dimension Match Thresholds
MATCH_THRESHOLDS = {
    "D2_direct_resume": 0.35,
    "D3_transferable_exp": 0.30,
    "D4_project_relevance": 0.25
}

# Positive Weights (Must sum to exactly 1.00)
WEIGHTS = {
    "D2_direct_resume": 0.20,
    "D3_transferable_exp": 0.15,
    "D4_project_relevance": 0.15,
    "D5_static_career_keyword_alignment": 0.10,
    "D6_title_closeness": 0.10,
    "D7_industry_closeness": 0.10,
    "D8_career_direction_alignment": 0.20
}

assert abs(sum(WEIGHTS.values()) - 1.00) < 1e-6, "Positive weights must sum to exactly 1.00"

EVIDENCE_STRENGTH_MULTIPLIERS = {
    "high": 1.00,
    "moderate": 0.70,
    "low": 0.35,
    "provenance_unverified": 0.00
}

PROTECTED_PHRASES = [
    "build-to-inventory", "process improvement", "continuous improvement",
    "multi-unit store operations", "operational excellence", "workflow automation",
    "business process automation", "agentic workflow", "district manager", "cost variance analysis"
]

GENERIC_SUPPRESSED_TERMS = {
    "operations", "leadership", "management", "systems", "process",
    "business", "strategy", "team", "work", "director", "manager", "specialist"
}

RELATED_TERM_GROUPS = {
    "continuous improvement": [
        ("continuous improvement", 1.0),
        ("process improvement", 0.9),
        ("operational excellence", 0.8),
        ("quality assurance", 0.6)
    ],
    "workflow automation": [
        ("workflow automation", 1.0),
        ("process automation", 0.9),
        ("business process automation", 0.8),
        ("agentic workflow", 0.8)
    ],
    "mcp": [
        ("model context protocol", 1.0),
        ("mcp server", 1.0),
        ("tool integration", 0.6)
    ]
}

NON_DEGREE_MASTER_PHRASES = [
    "scrum master", "master data", "master schedule", "master plan",
    "master agreement", "task mastery", "mastery"
]

RESUME_KEYWORDS = set([
    "multi-unit", "operations", "district", "manager", "p&l", "cost", "labor", "inventory",
    "leadership", "mentorship", "recruitment", "staffing", "retention", "qsc", "compliance",
    "turnaround", "forecasting", "build-to-inventory", "scheduling", "revenue", "sales",
    "six sigma", "yellow belt", "programming", "python", "systems", "governance", "process",
    "ai", "workflow", "automation", "mcp", "agentic", "dossiers", "telemetry"
])

BASE_DIR = Path(__file__).parent.resolve()
DEFAULT_REGISTRY_PATH = BASE_DIR / "career_evidence_registry.json"
DEFAULT_IDENTITY_PATH = BASE_DIR / "professional_identity_model.json"

def load_default_data(reg_path: Optional[Path] = None, id_path: Optional[Path] = None) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], List[str]]:
    r_path = reg_path or DEFAULT_REGISTRY_PATH
    i_path = id_path or DEFAULT_IDENTITY_PATH
    
    missing = []
    registry = None
    identity = None

    if r_path.is_file():
        try:
            with r_path.open("r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception as e:
            missing.append(f"{r_path.name} ({str(e)})")
    else:
        missing.append(r_path.name)

    if i_path.is_file():
        try:
            with i_path.open("r", encoding="utf-8") as f:
                identity = json.load(f)
        except Exception as e:
            missing.append(f"{i_path.name} ({str(e)})")
    else:
        missing.append(i_path.name)

    return registry, identity, missing

def parse_job_sections(job: Dict[str, Any]) -> Dict[str, Any]:
    title = (job.get("title") or "").lower()
    desc = (job.get("description") or "").lower()

    req_text = ""
    pref_text = ""
    resp_text = desc

    if "preferred" in desc or "desired" in desc:
        parts = re.split(r'\b(preferred|desired)\b', desc, flags=re.IGNORECASE)
        if len(parts) >= 3:
            resp_text = parts[0]
            pref_text = parts[2]

    if "requirements" in resp_text or "qualifications" in resp_text:
        parts = re.split(r'\b(requirements|qualifications)\b', resp_text, flags=re.IGNORECASE)
        if len(parts) >= 3:
            resp_text = parts[0]
            req_text = parts[2]

    all_text = f"{title} {desc}".lower()
    words = re.sub(r'[^a-z0-9\-\/\s]', ' ', all_text).split()
    valid_tokens = {w for w in words if len(w) > 2}
    specific_tokens = {t for t in valid_tokens if t not in GENERIC_SUPPRESSED_TERMS}

    return {
        "title": title,
        "resp_text": resp_text,
        "req_text": req_text,
        "pref_text": pref_text,
        "all_text": all_text,
        "valid_tokens": valid_tokens,
        "specific_tokens": specific_tokens,
        "found_phrases": {p for p in PROTECTED_PHRASES if p in all_text}
    }

def get_candidate_education_evidence(evidence_registry: Optional[Any]) -> List[str]:
    """Dynamically retrieves candidate education evidence IDs from the registry."""
    if not evidence_registry:
        return ["EV-EDU-001", "EV-EDU-002"]

    records = evidence_registry.get("evidence_records", []) if isinstance(evidence_registry, dict) else evidence_registry
    edu_ids = []
    for r in records:
        dom = (r.get("capability_domain") or "").lower()
        cap = (r.get("specific_capability") or "").lower()
        cls = (r.get("classification") or "").lower()
        if "education" in dom or "degree" in dom or "degree" in cap or cls == "supporting":
            edu_ids.append(r.get("evidence_id"))
    return edu_ids if edu_ids else ["EV-EDU-001", "EV-EDU-002"]

def check_requirements_v43(job: Dict[str, Any], section_data: Dict[str, Any], evidence_registry: Optional[Any] = None) -> Tuple[Optional[bool], List[str], List[Dict[str, Any]], float]:
    """
    Evaluates hard requirements independently.
    Phrase-independent preferred degree detection (handles 'Scrum Master' AND 'Master's degree preferred' in same description).
    """
    desc = section_data["all_text"]
    location = (job.get("location") or "").lower()
    pp = job.get("post_processing", {})
    loc_status = pp.get("location_status")
    is_remote = job.get("is_remote", False) or "remote" in location or "remote" in desc
    
    details = []
    failures = []
    penalty = 0.0

    # 1. Geographic / Commute Requirement
    if is_remote:
        details.append({
            "requirement_type": "Geographic / Commute",
            "requirement_text": "Work Location / Remote Status",
            "requirement_level": "required",
            "state": "not_applicable",
            "candidate_evidence_ids": ["EV-RES-001"],
            "reason": "Position confirmed remote; local commute radius not applicable",
            "confidence": 1.0
        })
    elif loc_status == "distance_out_of_range":
        dist = pp.get("distance_miles")
        msg = f"Location out of commute range ({dist}mi > 35mi)" if dist else "Location out of commute range"
        failures.append(msg)
        details.append({
            "requirement_type": "Geographic / Commute",
            "requirement_text": "35-mile Commute Radius",
            "requirement_level": "required",
            "state": "failed",
            "candidate_evidence_ids": [],
            "reason": msg,
            "confidence": 0.90
        })
    elif loc_status == "within_range":
        details.append({
            "requirement_type": "Geographic / Commute",
            "requirement_text": "35-mile Commute Radius",
            "requirement_level": "required",
            "state": "satisfied",
            "candidate_evidence_ids": ["EV-RES-001"],
            "reason": "Location confirmed within 35-mile commute radius",
            "confidence": 0.90
        })
    else:
        details.append({
            "requirement_type": "Geographic / Commute",
            "requirement_text": "Location Status Verification",
            "requirement_level": "required",
            "state": "unresolved",
            "candidate_evidence_ids": [],
            "reason": "Location status unverified; requires validation evidence",
            "confidence": 0.50
        })

    # 2. Hard Licenses
    if "pharmd" in desc or "registered pharmacist" in desc:
        failures.append("Requires Licensed Pharmacist (PharmD)")
        details.append({
            "requirement_type": "Professional License",
            "requirement_text": "PharmD / Active Pharmacist License",
            "requirement_level": "required",
            "state": "failed",
            "candidate_evidence_ids": [],
            "reason": "Active PharmD license mandatory for role",
            "confidence": 1.0
        })
    elif "pmp certification required" in desc or "must have pmp" in desc:
        failures.append("Requires Active PMP Certification")
        details.append({
            "requirement_type": "Professional Certification",
            "requirement_text": "PMP Certification",
            "requirement_level": "required",
            "state": "failed",
            "candidate_evidence_ids": [],
            "reason": "PMP certification mandatory",
            "confidence": 1.0
        })

    # 3. Phrase-Independent Preferred Degree Detection
    is_true_degree_preferred = bool(re.search(r"\b(master's degree|masters degree|mba|graduate degree)\b.*\bpreferred\b", desc))
    if is_true_degree_preferred:
        penalty += 5.0
        edu_ev_ids = get_candidate_education_evidence(evidence_registry)
        details.append({
            "requirement_type": "Education Level",
            "requirement_text": "Master's Degree / MBA Preferred",
            "requirement_level": "preferred",
            "state": "preferred_gap",
            "candidate_evidence_ids": edu_ev_ids,
            "reason": "Master's degree preferred; candidate holds A.A.S., B.A., M.A. (Biblical Studies)",
            "confidence": 0.85
        })

    if failures:
        return False, failures, details, penalty
    elif any(d["state"] == "unresolved" for d in details):
        return None, ["Job location or requirement status unresolved"], details, penalty
    else:
        return True, [], details, penalty

def route_evidence_dimension(record: Dict[str, Any]) -> Tuple[str, str, float, str]:
    """
    Metadata-driven evidence routing priority.
    Returns: (dimension, routing_basis, routing_confidence, rationale)
    Metadata remains authoritative. If ID-prefix fallback is used:
    routing_basis = "id_prefix_fallback", confidence reduced by 0.15.
    """
    eid = (record.get("evidence_id") or "").upper()
    src_val = (record.get("source_type") or "").lower()
    cls_val = (record.get("classification") or "").lower()
    rel_val = (record.get("evidence_relationship") or "").lower()
    dom_val = (record.get("capability_domain") or "").lower()

    # 1. Authoritative Metadata Checks
    if any(k in src_val for k in ["artifact", "software", "server", "pipeline", "code", "model"]) or rel_val in ["artifact_produced", "direct_author_and_architect"] or cls_val in ["project_governance", "supporting"]:
        return "D4_project_relevance", "metadata_authoritative", 1.00, "Routed by explicit artifact/project metadata"

    if cls_val == "direct" or "r\u00e9sum\u00e9" in src_val or "resume" in src_val or "multi-unit" in dom_val:
        return "D2_direct_resume", "metadata_authoritative", 1.00, "Routed by direct employment/resume metadata"

    if cls_val == "transferable" or "turnaround" in dom_val or "transformation" in dom_val:
        return "D3_transferable_exp", "metadata_authoritative", 1.00, "Routed by transferable leadership metadata"

    # 2. ID-Prefix Fallback
    if eid.startswith(("EV-MCP", "EV-SOUL", "EV-PIPE", "EV-GTK", "EV-DEV", "EV-FID", "EV-AUD", "EV-PRD", "EV-REP")):
        return "D4_project_relevance", "id_prefix_fallback", 0.85, f"Routed by ID prefix fallback ({eid})"
    elif eid.startswith(("EV-RES", "EV-LNK")):
        return "D2_direct_resume", "id_prefix_fallback", 0.85, f"Routed by ID prefix fallback ({eid})"
    elif eid.startswith(("EV-WDS", "EV-CAS", "EV-LEAD")):
        return "D3_transferable_exp", "id_prefix_fallback", 0.85, f"Routed by ID prefix fallback ({eid})"

    return "D4_project_relevance", "id_prefix_fallback", 0.70, "Default fallback dimension"

def compute_hybrid_match_score(record: Dict[str, Any], section_data: Dict[str, Any]) -> Tuple[float, float, List[str]]:
    if record.get("provenance_unverified") is True or record.get("evidence_strength") == "provenance_unverified":
        return 0.0, 0.0, ["Rejected: Unverified provenance"]

    text_fields = [
        record.get("specific_capability", ""),
        record.get("work_performed", ""),
        record.get("business_or_operational_relevance", ""),
        record.get("exact_source_excerpt", "")
    ]
    tools = record.get("technical_tools", [])
    if isinstance(tools, list):
        text_fields.extend(tools)

    rec_text = " ".join([str(f) for f in text_fields]).lower()
    rec_tokens = set(re.sub(r'[^a-z0-9\-\/\s]', ' ', rec_text).split())
    specific_rec_tokens = {t for t in rec_tokens if t not in GENERIC_SUPPRESSED_TERMS and len(t) > 2}

    if not specific_rec_tokens:
        return 0.0, 0.0, []

    matched_tokens = specific_rec_tokens.intersection(section_data["specific_tokens"])
    if not matched_tokens:
        return 0.0, 0.0, []

    ev_coverage = len(matched_tokens) / len(specific_rec_tokens)
    job_req_coverage = len(matched_tokens) / len(section_data["specific_tokens"]) if section_data["specific_tokens"] else 0.0

    phrase_score = 0.0
    matched_phrases = []
    for phrase in section_data["found_phrases"]:
        if phrase in rec_text:
            phrase_score += 0.50
            matched_phrases.append(phrase)
    phrase_score = min(1.0, phrase_score)

    related_score = 0.0
    for group_key, term_list in RELATED_TERM_GROUPS.items():
        if group_key in rec_text:
            for term, credit in term_list:
                if term in section_data["all_text"]:
                    related_score = max(related_score, credit)

    raw_score = round(min(1.00, 0.35 * min(1.0, ev_coverage * 2.0) + 0.30 * min(1.0, job_req_coverage * 4.0) + 0.20 * phrase_score + 0.15 * related_score), 3)

    strength = (record.get("evidence_strength") or "moderate").lower()
    mult = EVIDENCE_STRENGTH_MULTIPLIERS.get(strength, 0.70)
    adjusted_score = round(raw_score * mult, 3)

    all_matched_terms = list(set(list(matched_tokens)[:3] + matched_phrases))
    return raw_score, adjusted_score, all_matched_terms

def resolve_evidence_groups(matched_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for item in matched_items:
        rec = item["record"]
        eid = rec.get("evidence_id", "")
        source_path = rec.get("source_path", "")
        related = item.get("related_ids", [])

        if related:
            group_key = sorted([eid] + related)[0]
        elif source_path:
            group_key = source_path
        elif "-" in eid:
            group_key = "-".join(eid.split("-")[:2])
        else:
            group_key = eid

        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)
    return groups

def calculate_capped_dimension_score(groups: Dict[str, List[Dict[str, Any]]], dim_name: str) -> Tuple[float, List[Dict[str, Any]]]:
    if not groups:
        return 0.00, []

    sorted_groups = []
    for g_key, items in groups.items():
        best_item = max(items, key=lambda x: x["adjusted_match_score"])
        sorted_groups.append((g_key, best_item))

    sorted_groups.sort(key=lambda x: x[1]["adjusted_match_score"], reverse=True)

    g1_score = sorted_groups[0][1]["adjusted_match_score"]
    g2_score = sorted_groups[1][1]["adjusted_match_score"] if len(sorted_groups) > 1 else 0.0
    g3_score = sorted_groups[2][1]["adjusted_match_score"] if len(sorted_groups) > 2 else 0.0

    combined_score = round(min(1.00, g1_score + 0.25 * g2_score + 0.10 * g3_score), 3)

    citations = []
    for g_key, best_item in sorted_groups[:3]:
        rec = best_item["record"]
        routing_info = best_item.get("routing_info", ("dim", "metadata_authoritative", 1.0, "metadata"))
        citations.append({
            "evidence_id": rec.get("evidence_id"),
            "dimension_supported": dim_name,
            "evidence_strength": rec.get("evidence_strength", "moderate"),
            "classification": rec.get("classification", "direct"),
            "evidence_relationship": rec.get("evidence_relationship", "reported_by_candidate"),
            "routing_basis": routing_info[1],
            "routing_confidence": routing_info[2],
            "matching_rationale": f"Matched terms ({', '.join(best_item['matched_terms'][:3])}) in {rec.get('specific_capability')} [{routing_info[3]}]",
            "limitation": rec.get("limitations", "None documented"),
            "source_path": rec.get("source_path", "registry"),
            "distinct_evidence_group": g_key,
            "raw_match_score": round(best_item["raw_match_score"], 2),
            "adjusted_match_score": round(best_item["adjusted_match_score"], 2)
        })

    return combined_score, citations

def compute_evidence_confidence_breakdown(citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not citations:
        return {
            "strength_distribution": {"high_count": 0, "moderate_count": 0, "low_count": 0},
            "source_authority": {"candidate_reported_count": 0, "author_architect_count": 0, "artifact_count": 0},
            "dimension_coverage": {"d2_active": False, "d3_active": False, "d4_active": False},
            "confidence_score": 0.00,
            "confidence_level": "Low"
        }

    high_c = sum(1 for c in citations if c.get("evidence_strength") == "high")
    mod_c = sum(1 for c in citations if c.get("evidence_strength") == "moderate")
    low_c = sum(1 for c in citations if c.get("evidence_strength") == "low")

    cand_c = sum(1 for c in citations if c.get("evidence_relationship") == "reported_by_candidate")
    auth_c = sum(1 for c in citations if c.get("evidence_relationship") == "direct_author_and_architect")
    art_c = sum(1 for c in citations if c.get("evidence_relationship") == "artifact_produced")

    d2_act = any(c.get("dimension_supported") == "D2_direct_resume" for c in citations)
    d3_act = any(c.get("dimension_supported") == "D3_transferable_exp" for c in citations)
    d4_act = any(c.get("dimension_supported") == "D4_project_relevance" for c in citations)

    cov_ratio = (int(d2_act) + int(d3_act) + int(d4_act)) / 3.0
    str_score = (high_c * 1.0 + mod_c * 0.7 + low_c * 0.35) / len(citations)

    conf_score = round(0.50 * str_score + 0.50 * cov_ratio, 2)
    level = "High" if conf_score >= 0.70 else ("Moderate" if conf_score >= 0.40 else "Low")

    return {
        "strength_distribution": {"high_count": high_c, "moderate_count": mod_c, "low_count": low_c},
        "source_authority": {"candidate_reported_count": cand_c, "author_architect_count": auth_c, "artifact_count": art_c},
        "dimension_coverage": {"d2_active": d2_act, "d3_active": d3_act, "d4_active": d4_act},
        "confidence_score": conf_score,
        "confidence_level": level
    }

def determine_fit_recommendation_and_policy_trace(
    eligibility_disp: Optional[bool],
    pbs_score: float,
    lane_id: str,
    d6_score: float,
    d8_score: float,
    conf_breakdown: Dict[str, Any],
    citations: List[Dict[str, Any]],
    unresolved_reqs: List[str],
    is_incomplete_posting: bool
) -> Tuple[str, Dict[str, Any]]:
    """
    Decoupled 5-tier recommendation policy engine.
    """
    conf_level = conf_breakdown.get("confidence_level", "Low")
    conf_score = conf_breakdown.get("confidence_score", 0.0)
    cov = conf_breakdown.get("dimension_coverage", {})
    active_dims_count = sum(1 for active in cov.values() if active)
    supported_dims = [dim for dim, active in cov.items() if active]

    pbs_pass = pbs_score >= 50.0
    lane_resolved = lane_id not in ["Unresolved", ""] and "fallback" not in lane_id
    lane_any_resolved = lane_id not in ["Unresolved", ""]
    title_align = d6_score >= 0.70
    career_align = d8_score >= 0.80

    decisive_rules = []
    recommendation = "Do Not Prioritize"

    # 1. Ineligible Gate
    if eligibility_disp is False:
        recommendation = "Do Not Apply — Ineligible"
        decisive_rules.append("Candidate failed mandatory hard requirement gate")
    
    # 2. Manual Review Gate
    elif eligibility_disp is None or is_incomplete_posting or len(unresolved_reqs) > 0:
        recommendation = "Manual Review"
        if is_incomplete_posting:
            decisive_rules.append("Incomplete job description posting details")
        if len(unresolved_reqs) > 0:
            decisive_rules.append(f"Unresolved material requirements: {', '.join(unresolved_reqs)}")
    
    # 3. Priority Application Gate
    elif (
        eligibility_disp is True
        and pbs_score >= 65.0
        and lane_resolved
        and title_align
        and career_align
        and conf_score >= 0.40
        and active_dims_count >= 2
    ):
        recommendation = "Priority Application"
        decisive_rules.append("PBS score >= 65.0, fully resolved lane, strong title & career alignment, >=2 active dimensions")

    # 4. Consider Application Gate
    elif (
        eligibility_disp is True
        and pbs_score >= 50.0
        and lane_any_resolved
        and conf_score >= 0.40
        and active_dims_count >= 1
    ):
        recommendation = "Consider Application"
        decisive_rules.append("PBS score >= 50.0, resolved/governed lane, moderate confidence, >=1 active evidence dimension")

    # 5. Do Not Prioritize (Default Eligible Fallback)
    else:
        recommendation = "Do Not Prioritize"
        if pbs_score < 50.0:
            decisive_rules.append("PBS fit score below minimum 50.0 application threshold")
        if not lane_any_resolved:
            decisive_rules.append("Unresolved career identity lane alignment")
        if active_dims_count < 1:
            decisive_rules.append("Insufficient active evidence dimension coverage")

    trace = {
        "pbs_threshold_pass": pbs_pass,
        "eligibility_pass": eligibility_disp,
        "lane_resolution": lane_id,
        "title_alignment": d6_score,
        "career_direction": d8_score,
        "evidence_confidence": conf_level,
        "supported_dimensions": supported_dims,
        "unresolved_requirements": unresolved_reqs,
        "decisive_rules": decisive_rules
    }

    return recommendation, trace

def evaluate_job(
    job: Dict[str, Any],
    evidence_registry: Optional[Any] = None,
    identity_model: Optional[Dict[str, Any]] = None,
    reg_path: Optional[Path] = None,
    id_path: Optional[Path] = None
) -> Dict[str, Any]:

    default_reg, default_id, missing_files = load_default_data(reg_path, id_path)

    if evidence_registry is None:
        evidence_registry = default_reg
    if identity_model is None:
        identity_model = default_id

    # Missing input files handling
    if evidence_registry is None or identity_model is None:
        missing_name = missing_files[0] if missing_files else "missing_file"
        return {
            "job_id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company"),
            "score_status": "incomplete",
            "eligibility_disposition": None,
            "eligible": None,
            "fit_recommendation": "Manual Review",
            "recommendation_status": "Manual Review",
            "strategic_value": "Insufficient Information",
            "missing_inputs": missing_files if missing_files else [missing_name],
            "pbs_job_fit_score_pre_calibration": 0.0,
            "diagnostic_fit_score": 0.0,
            "capability_fit_score": 0.0,
            "market_readiness_fit_score": 0.0,
            "evidence_citations": []
        }

    desc = job.get("description") or ""
    title = job.get("title") or ""

    is_incomplete_posting = not desc or len(desc.split()) < 5

    if is_incomplete_posting:
        return {
            "job_id": job.get("id"),
            "title": title,
            "company": job.get("company"),
            "score_status": "incomplete",
            "eligibility_disposition": None,
            "eligible": None,
            "fit_recommendation": "Manual Review",
            "recommendation_status": "Manual Review",
            "strategic_value": "Insufficient Information",
            "missing_inputs": ["job_description_incomplete"],
            "pbs_job_fit_score_pre_calibration": 0.0,
            "diagnostic_fit_score": 0.0,
            "capability_fit_score": 0.0,
            "market_readiness_fit_score": 0.0,
            "evidence_citations": []
        }

    # 1. Section Parsing & Requirements
    section_data = parse_job_sections(job)
    eligibility_disp, failure_reasons, req_details, penalty = check_requirements_v43(job, section_data, evidence_registry)

    unresolved_reqs = [r["requirement_type"] for r in req_details if r.get("state") == "unresolved"]

    # 2. Hybrid Evidence Matching
    records = []
    if isinstance(evidence_registry, dict) and "evidence_records" in evidence_registry:
        records = evidence_registry["evidence_records"]
    elif isinstance(evidence_registry, list):
        records = evidence_registry

    d2_items = []
    d3_items = []
    d4_items = []

    for rec in records:
        raw_score, adj_score, terms = compute_hybrid_match_score(rec, section_data)
        dim_target, basis, conf_mult, rat = route_evidence_dimension(rec)

        threshold = MATCH_THRESHOLDS.get(dim_target, 0.25)
        if adj_score >= threshold:
            item = {
                "record": rec,
                "raw_match_score": raw_score,
                "adjusted_match_score": adj_score,
                "matched_terms": terms,
                "related_ids": rec.get("related_evidence_ids", []),
                "routing_info": (dim_target, basis, conf_mult, rat)
            }
            if dim_target == "D2_direct_resume":
                d2_items.append(item)
            elif dim_target == "D3_transferable_exp":
                d3_items.append(item)
            else:
                d4_items.append(item)

    d2_score, d2_cites = calculate_capped_dimension_score(resolve_evidence_groups(d2_items), "D2_direct_resume")
    d3_score, d3_cites = calculate_capped_dimension_score(resolve_evidence_groups(d3_items), "D3_transferable_exp")
    d4_score, d4_cites = calculate_capped_dimension_score(resolve_evidence_groups(d4_items), "D4_project_relevance")

    # 3. Identity Model & Horizon Resolution (Unknown Role Default -> Unresolved / 0.00 / Insufficient Information)
    title_lower = title.lower()
    title_norm = title_lower.replace("operational", "operations")
    lanes = identity_model.get("professional_identity_lanes", {})

    lane_id = "Unresolved"
    lane_name = "Unresolved"
    horizon = "Unresolved"
    d8_score = 0.00
    d6_score = 0.00
    found_in_model = False

    for l_key, l_data in lanes.items():
        name = l_data.get("name", l_key)
        horizons = l_data.get("target_role_horizons", {})
        for h_key, titles_list in horizons.items():
            for t_targ in titles_list:
                t_norm = t_targ.lower().replace("operational", "operations")
                if t_norm in title_norm or title_norm in t_norm:
                    lane_id, lane_name, horizon = l_key, name, h_key
                    d8_score = 0.85 if h_key == "immediate_market_targets" else (0.90 if h_key == "stretch_targets" else 1.00)
                    d6_score = 0.80 if h_key == "immediate_market_targets" else (0.70 if h_key == "stretch_targets" else 0.60)
                    found_in_model = True
                    break
            if found_in_model:
                break
        if found_in_model:
            break

    # Governed secondary fallbacks
    if not found_in_model:
        if "district manager" in title_lower or "multi-unit" in title_lower:
            lane_id, lane_name, horizon, d8_score, d6_score = "Lane_A", "Direct Operations Leadership (lane_fallback)", "immediate_market_targets", 0.50, 0.50
        elif "process improvement" in title_lower or "operations transformation" in title_lower:
            lane_id, lane_name, horizon, d8_score, d6_score = "Lane_B", "Operations Systems (lane_fallback)", "immediate_market_targets", 0.60, 0.50
        elif "ai enablement" in title_lower or "workflow automation" in title_lower:
            lane_id, lane_name, horizon, d8_score, d6_score = "Lane_C", "Applied AI (lane_fallback)", "immediate_market_targets", 0.70, 0.50

    # 4. Industry Closeness
    desc_lower = desc.lower()
    if any(ind in desc_lower for ind in ["restaurant", "qsr", "food service", "multi-unit retail", "store operations"]):
        d7_score, ind_status = 0.85, "confirmed_close"
    elif any(ind in desc_lower for ind in ["logistics", "supply chain", "hospitality", "customer operations"]):
        d7_score, ind_status = 0.65, "transferable"
    elif any(ind in desc_lower for ind in ["particle physics", "aerospace hardware", "clinical nursing"]):
        d7_score, ind_status = 0.20, "confirmed_distant"
    else:
        d7_score, ind_status = 0.00, "unresolved"

    # 5. D5 Static Keyword Alignment
    desc_words = set(section_data["valid_tokens"])
    overlap = RESUME_KEYWORDS.intersection(desc_words)
    d5_score = round(min(1.00, (len(overlap) / len(RESUME_KEYWORDS)) * 1.8), 3)

    # Positive Fit Score (Scale 0-100)
    raw_positive_sum = 100.0 * (
        WEIGHTS["D2_direct_resume"] * d2_score +
        WEIGHTS["D3_transferable_exp"] * d3_score +
        WEIGHTS["D4_project_relevance"] * d4_score +
        WEIGHTS["D5_static_career_keyword_alignment"] * d5_score +
        WEIGHTS["D6_title_closeness"] * d6_score +
        WEIGHTS["D7_industry_closeness"] * d7_score +
        WEIGHTS["D8_career_direction_alignment"] * d8_score
    )

    positive_fit_score = round(raw_positive_sum, 1)

    cap_sum_w = WEIGHTS["D2_direct_resume"] + WEIGHTS["D3_transferable_exp"] + WEIGHTS["D4_project_relevance"] + WEIGHTS["D5_static_career_keyword_alignment"]
    capability_fit_score = round(((
        WEIGHTS["D2_direct_resume"] * d2_score +
        WEIGHTS["D3_transferable_exp"] * d3_score +
        WEIGHTS["D4_project_relevance"] * d4_score +
        WEIGHTS["D5_static_career_keyword_alignment"] * d5_score
    ) / cap_sum_w) * 100.0, 1)

    mkt_sum_w = WEIGHTS["D6_title_closeness"] + WEIGHTS["D7_industry_closeness"]
    market_readiness_fit_score = round(((
        WEIGHTS["D6_title_closeness"] * d6_score +
        WEIGHTS["D7_industry_closeness"] * d7_score
    ) / mkt_sum_w) * 100.0, 1)

    diagnostic_fit_score = round(max(0.0, min(100.0, positive_fit_score - penalty)), 1)
    final_pbs_score = 0.0 if eligibility_disp is False else diagnostic_fit_score

    all_citations = d2_cites + d3_cites + d4_cites
    conf_breakdown = compute_evidence_confidence_breakdown(all_citations)

    # Fit Recommendation & Policy Trace
    fit_recommendation, policy_trace = determine_fit_recommendation_and_policy_trace(
        eligibility_disp, final_pbs_score, lane_id, d6_score, d8_score,
        conf_breakdown, all_citations, unresolved_reqs, is_incomplete_posting
    )

    # Independent Strategic Value
    if eligibility_disp is False:
        strategic_value = "Not Evaluated — Ineligible"
    elif lane_id == "Unresolved":
        strategic_value = "Insufficient Information"
    elif final_pbs_score >= 65.0 and d8_score >= 0.80:
        strategic_value = "Career Advancing"
    elif final_pbs_score >= 50.0:
        strategic_value = "Career Maintaining"
    else:
        strategic_value = "Income Stabilizing"

    return {
        "job_id": job.get("id"),
        "title": title,
        "company": job.get("company"),
        "location": job.get("location"),
        "score_status": "complete",
        "eligibility_disposition": eligibility_disp,
        "eligible": eligibility_disp,
        "fit_recommendation": fit_recommendation,
        "recommendation_status": fit_recommendation,
        "recommendation_policy_trace": policy_trace,
        "professional_lane": lane_id,
        "professional_lane_name": lane_name,
        "target_role_horizon": horizon,
        "hard_requirement_failures": failure_reasons,
        "requirement_details": req_details,
        "pbs_job_fit_score_pre_calibration": final_pbs_score,
        "diagnostic_fit_score": diagnostic_fit_score,
        "capability_fit_score": capability_fit_score,
        "market_readiness_fit_score": market_readiness_fit_score,
        "strategic_value": strategic_value,
        "evidence_confidence": conf_breakdown["confidence_level"],
        "evidence_confidence_breakdown": conf_breakdown,
        "industry_match_status": ind_status,
        "dimension_scores": {
            "D2_direct_resume": round(d2_score, 2),
            "D3_transferable_exp": round(d3_score, 2),
            "D4_project_relevance": round(d4_score, 2),
            "D5_static_career_keyword_alignment": round(d5_score, 2),
            "D6_title_closeness": round(d6_score, 2),
            "D7_industry_closeness": round(d7_score, 2),
            "D8_career_direction_alignment": round(d8_score, 2)
        },
        "evidence_citations": all_citations
    }

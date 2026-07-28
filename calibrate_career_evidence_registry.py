import json

REGISTRY_PATH = r"D:\blogger\jobspy-mcp-server\career_evidence_registry.json"

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

records = data["evidence_records"]

# Calibrate each record
for r in records:
    eid = r["evidence_id"]
    stype = r.get("source_type", "")
    
    # 1. Authorship & Evidence Relationship calibration
    if stype in ["Verified résumé record", "Public Profile Record"]:
        r["authorship_status"] = "not_applicable"
        if stype == "Public Profile Record":
            r["evidence_relationship"] = "public_profile_owned_by_candidate"
        elif "Degree" in r.get("specific_capability", "") or "Education" in r.get("specific_capability", ""):
            r["evidence_relationship"] = "credential_held_by_candidate"
        else:
            r["evidence_relationship"] = "reported_by_candidate"
    elif "woods_gatekeeper.py" in r.get("source_path", ""):
        r["authorship_status"] = "directed_ai_assisted"
        r["evidence_relationship"] = "directed_by_candidate"
    elif "principles.json" in r.get("source_path", ""):
        r["authorship_status"] = "directed_ai_assisted"
        r["evidence_relationship"] = "designed_by_candidate"
    elif "post_processor.py" in r.get("source_path", "") or "pbs_fit_scorer.py" in r.get("source_path", ""):
        r["authorship_status"] = "directed_ai_assisted"
        r["evidence_relationship"] = "designed_by_candidate"
    elif "configured_integrated" in r.get("authorship_status", ""):
        r["evidence_relationship"] = "configured_by_candidate"
    elif "personally_authored" in r.get("authorship_status", ""):
        r["evidence_relationship"] = "designed_by_candidate"
    else:
        r["evidence_relationship"] = "directed_by_candidate"

    # 2. Resume Outcome calibration (Rule #5)
    if stype == "Verified résumé record" and "EV-RES" in eid:
        r["artifact_evidence"] = "The résumé contains the stated claim."
        r["implementation_evidence"] = "The résumé describes the role, action, or implementation."
        r["outcome_evidence"] = "Self-reported professional outcome requiring employer records, references, performance reports, or other corroboration for independent verification."
        r["evidence_strength"] = "moderate"  # Calibrated: self-reported career claim without independent outcome corroboration

    # 3. Education / Credentials calibration
    if stype == "Verified résumé record" and "EV-EDU" in eid:
        r["artifact_evidence"] = "The résumé contains the stated academic credential."
        r["implementation_evidence"] = "The résumé lists degree program completion."
        r["outcome_evidence"] = "Self-reported academic credential requiring institutional verification for independent audit."
        r["evidence_strength"] = "high"  # High for degree completion claim on resume

    # 4. EV-MCP-004 Rename (Rule #3)
    if eid == "EV-MCP-004":
        r["specific_capability"] = "Pre-Calibration PBS Job Fit Scorer Engine (pbs_fit_scorer.py)"
        r["evidence_strength"] = "moderate"  # Moderate: executable script present, but scores are pre-calibration pending hiring outcome data
        r["limitations"] = "Pre-calibration fit model; empirical calibration requires real application submission and hiring outcome data."

    # 5. EV-CAS-001 Correction (Rule #4)
    if eid == "EV-CAS-001":
        r["capability_domain"] = "Organizational Systems Diagnosis & Operational Case Analysis"
        r["specific_capability"] = "Operational Case Formalization — Voluntary Extension Case"
        r["work_performed"] = "Documented an operational case in which aligned incentives were associated with voluntary discretionary effort."
        r["verified_outcome"] = "Documented operational case illustrating aligned incentives and voluntary discretionary effort; case-based support only, not universal empirical proof."
        r["evidence_strength"] = "moderate"

    # 6. Evidence strength calibration for software/spec artifacts
    if "EV-WDS" in eid or "EV-FID" in eid or "EV-GTK" in eid:
        if eid in ["EV-GTK-001", "EV-WDS-001", "EV-WDS-002", "EV-FID-001"]:
            r["evidence_strength"] = "high"  # Directly grounded canonical/software specs
        else:
            r["evidence_strength"] = "moderate"
    elif "EV-SOUL" in eid or "EV-PIPE" in eid or "EV-MCP" in eid:
        if eid in ["EV-MCP-001", "EV-MCP-002", "EV-MCP-003"]:
            r["evidence_strength"] = "high"  # Executable source code with documented test runs
        else:
            r["evidence_strength"] = "moderate"
    elif "EV-DEV" in eid or "EV-AUD" in eid or "EV-SOV" in eid or "EV-JUS" in eid or "EV-OPM" in eid or "EV-POD" in eid or "EV-RDT" in eid or "EV-MKT" in eid or "EV-NWS" in eid or "EV-REP" in eid or "EV-DFT" in eid or "EV-SYS" in eid or "EV-NCH" in eid or "EV-GRW" in eid:
        r["evidence_strength"] = "low" if "configured" in r["authorship_status"] or "unverified" in r.get("outcome_evidence", "") else "moderate"

    # Fix LinkedIn profile record
    if eid == "EV-LNK-001":
        r["authorship_status"] = "not_applicable"
        r["evidence_relationship"] = "public_profile_owned_by_candidate"
        r["evidence_strength"] = "moderate"

data["total_evidence_records"] = len(records)
data["generated_at"] = "2026-07-27T15:45:00Z"

with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Registry successfully calibrated for all {len(records)} records.")

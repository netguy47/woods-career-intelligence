import json
import os

REGISTRY_PATH = r"D:\blogger\jobspy-mcp-server\career_evidence_registry.json"
IDENTITY_PATH = r"D:\blogger\jobspy-mcp-server\professional_identity_model.json"

def apply_registry_corrections():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for record in data["evidence_records"]:
        eid = record.get("evidence_id")
        
        # Correction 1: EV-MCP-001
        if eid == "EV-MCP-001":
            record["verified_outcome"] = "Registered in the Antigravity MCP configuration and successfully executed live job-retrieval logic. End-to-end client invocation evidence was not preserved."
            record["implementation_evidence"] = "Source code, server configuration, subprocess execution, and saved job output support local integration and retrieval."
            record["outcome_evidence"] = "Job retrieval is confirmed. End-to-end MCP client transport remains partially verified."
            record["evidence_strength"] = "moderate"
            print("Corrected EV-MCP-001")

        # Correction 2: EV-LNK-001
        elif eid == "EV-LNK-001":
            record["artifact_evidence"] = "Records the LinkedIn profile URL and profile content reported during authorized access."
            record["outcome_evidence"] = "Profile-history consistency was reported but is not independently verifiable from the frozen snapshot because no profile capture was preserved."
            print("Corrected EV-LNK-001")

        # Correction 3: EV-EDU-001 & EV-EDU-002
        elif eid in ["EV-EDU-001", "EV-EDU-002"]:
            record["evidence_strength"] = "moderate"
            print(f"Corrected strength for {eid}")

        # Correction 4: Audit deployment language for SOUL, AUD, REP, etc.
        if "externally deployed" in (record.get("verified_outcome") or "").lower():
            record["verified_outcome"] = record["verified_outcome"].replace("externally deployed", "locally implemented")
            print(f"Audited deployment wording in {eid}")

    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Updated career_evidence_registry.json")

def apply_identity_corrections():
    with open(IDENTITY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Correction 5: Lane A rationale
    lane_a = data["professional_identity_lanes"]["Lane_A"]
    lane_a["confidence_rationale"] = lane_a["confidence_rationale"].replace(
        "verified multi-unit district management",
        "documented and self-reported multi-unit operations leadership"
    )

    # Correction 6: Lane B target roles
    lane_b_targets = data["professional_identity_lanes"]["Lane_B"]["target_role_horizons"]
    if "Operations Excellence Manager" in lane_b_targets["immediate_market_targets"]:
        lane_b_targets["immediate_market_targets"].remove("Operations Excellence Manager")
        if "Operations Excellence Manager" not in lane_b_targets["stretch_targets"]:
            lane_b_targets["stretch_targets"].insert(0, "Operations Excellence Manager")

    new_bridge_targets = [
        "Continuous Improvement Specialist",
        "Process Improvement Analyst",
        "Operations Implementation Specialist"
    ]
    for target in new_bridge_targets:
        if target not in lane_b_targets["immediate_market_targets"]:
            lane_b_targets["immediate_market_targets"].append(target)

    with open(IDENTITY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Updated professional_identity_model.json")

if __name__ == "__main__":
    apply_registry_corrections()
    apply_identity_corrections()

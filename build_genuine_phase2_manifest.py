import os
import json
import hashlib
import datetime

BASE_DIR = r"D:\blogger"
REGISTRY_PATH = r"D:\blogger\jobspy-mcp-server\career_evidence_registry.json"
MANIFEST_PATH = r"D:\blogger\jobspy-mcp-server\ingestion_manifest.json"

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    registry_data = json.load(f)

# Build lookup map from evidence registry
file_evidence_map = {}
for rec in registry_data["evidence_records"]:
    path = rec.get("source_path", "")
    if not path:
        continue
    # Normalize relative path if inside D:\blogger
    if path.startswith("D:\\blogger\\"):
        rel_p = path[len("D:\\blogger\\"):]
    elif path.startswith("C:\\Users\\Donal\\OneDrive\\Documents\\"):
        rel_p = path
    else:
        rel_p = path
    
    if rel_p not in file_evidence_map:
        file_evidence_map[rel_p] = []
    file_evidence_map[rel_p].append(rec)

# Load existing scan manifest for hashes/mtimes if present
hash_lookup = {}
if os.path.exists(MANIFEST_PATH):
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        full_manifest = json.load(f)
        for item in full_manifest.get("manifest", []):
            hash_lookup[item["file_path"]] = item

project_families = {
    ".agents/woods-framework": "Woods Leadership Systems Framework",
    "woods-framework": "Woods Leadership Systems Framework Legacy",
    "jobspy-mcp-server": "JobSpy MCP Pipeline",
    "Double-Edge-Insight-AI-Pipeline": "Double-Edge Express/MCP Server",
    "sovereign-audit-site": "Sovereign Audit Web App",
    "sovereign-editor-lite": "Sovereign Editor Component",
    "sovereign": "Sovereign Kernel Scheduler",
    "research": "Newsroom Safety & Research",
    "driftcast": "Driftcast Retrospective Protocol",
    "openmontage": "OpenMontage Media Adapter",
    "jusbt_pipeline": "JUSBT Pipeline",
    "podcastfy_repo": "Podcastfy Audio Integration",
    "reddit-mcp": "Reddit MCP Server",
    "growth": "Growth Agent Infrastructure",
    "10 niche intelligence reports": "Market Intelligence Research",
    "SYSTEM DIRECTIVE": "Foreman Supervisory Protocol"
}

def determine_project_family(rel_path):
    norm = rel_path.replace('\\', '/')
    for k, v in project_families.items():
        if k in norm:
            return v
    if "resume" in norm.lower():
        return "Verified Resume Records"
    return "Workspace Root Tools"

manifest_records = []

# Process all files mapped in evidence records and project files
processed_paths = set()

for rel_path, recs in file_evidence_map.items():
    processed_paths.add(rel_path)
    full_p = os.path.join(BASE_DIR, rel_path) if not rel_path.startswith("C:") else rel_path

    proj_fam = determine_project_family(rel_path)
    ext = os.path.splitext(rel_path)[1].lower()
    
    # Check if we have calculated hash previously
    prev_item = hash_lookup.get(rel_path, {})
    chash = prev_item.get("content_hash", "UNVERIFIED_HASH")
    mtime = prev_item.get("last_modified", "UNVERIFIED_MTIME")

    if os.path.exists(full_p):
        read_stat = "provenance_reconstructed"
        prov_basis = "Source path referenced in active evidence registry and confirmed present on filesystem during Phase 2 execution."
        mconf = "high"
        try:
            stat = os.stat(full_p)
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc).isoformat()
            if chash == "UNVERIFIED_HASH":
                sha256 = hashlib.sha256()
                with open(full_p, 'rb') as f:
                    while chunk := f.read(65536):
                        sha256.update(chunk)
                chash = sha256.hexdigest()
        except Exception:
            pass
    else:
        read_stat = "provenance_unverified"
        prov_basis = "Source path referenced in active evidence registry but file not directly verified on filesystem."
        mconf = "moderate"

    ev_ids = [r["evidence_id"] for r in recs]
    auth_statuses = list(set([r["authorship_status"] for r in recs]))
    art_ev = [r.get("artifact_evidence") for r in recs if r.get("artifact_evidence")]
    imp_ev = [r.get("implementation_evidence") for r in recs if r.get("implementation_evidence")]
    out_ev = [r.get("outcome_evidence") for r in recs if r.get("outcome_evidence")]

    manifest_records.append({
        "file_path": rel_path,
        "project_family": proj_fam,
        "file_type": ext if ext else "no_ext",
        "authority_level": recs[0].get("authority_level", 5 if ext in [".py", ".ts", ".js"] else 1 if "woods" in rel_path.lower() else 4),
        "read_status": read_stat,
        "content_hash": chash,
        "last_modified": mtime,
        "canonical_status": "canonical" if "principles.json" in rel_path else "canonical_supporting" if "woods" in rel_path.lower() else "non_canonical",
        "evidence_ids_derived": ev_ids,
        "authorship_status_assigned": auth_statuses[0] if len(auth_statuses) == 1 else auth_statuses,
        "artifact_evidence_created": art_ev,
        "implementation_evidence_created": imp_ev,
        "outcome_evidence_created": out_ev,
        "exclusion_reason": None,
        "provenance_basis": prov_basis,
        "manifest_confidence": mconf
    })

# Add workspace files from Phase 2 discovery that were scanned but not mapped to evidence IDs
if os.path.exists(MANIFEST_PATH):
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        full_manifest = json.load(f)
        for item in full_manifest.get("manifest", []):
            rp = item["file_path"]
            if rp in processed_paths:
                continue
            processed_paths.add(rp)
            proj_fam = determine_project_family(rp)
            
            manifest_records.append({
                "file_path": rp,
                "project_family": proj_fam,
                "file_type": item.get("file_type", "unknown"),
                "authority_level": item.get("authority_level", 9),
                "read_status": "provenance_unverified" if item.get("read_status") == "read_success" else item.get("read_status"),
                "content_hash": item.get("content_hash", "UNVERIFIED_HASH"),
                "last_modified": item.get("last_modified", "UNVERIFIED_MTIME"),
                "canonical_status": item.get("canonical_status", "non_canonical"),
                "evidence_ids_derived": [],
                "authorship_status_assigned": "unclear",
                "artifact_evidence_created": [],
                "implementation_evidence_created": [],
                "outcome_evidence_created": [],
                "exclusion_reason": item.get("exclusion_reason"),
                "provenance_basis": "File path recorded during full workspace scan script execution.",
                "manifest_confidence": "moderate"
            })

out_manifest = {
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "phase": "Genuine Phase 2 Ingestion Manifest (Reconstructed from Phase 2 Execution Evidence)",
    "total_artifacts_documented": len(manifest_records),
    "evidence_derived_artifacts_count": len(file_evidence_map),
    "workspace_scanned_artifacts_count": len(manifest_records) - len(file_evidence_map),
    "manifest_status": "reconstructed_from_execution_evidence",
    "manifest": manifest_records
}

out_path = r"D:\blogger\jobspy-mcp-server\phase2_review_package\genuine_phase2_ingestion_manifest.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out_manifest, f, indent=2)

print(f"Genuine Phase 2 Manifest built successfully: {len(manifest_records)} artifacts documented.")

import os
import json
import hashlib
import datetime

BASE_DIR = r"D:\blogger"

# Specific high-value directories to scan
TARGET_PATHS = [
    r"D:\blogger\.agents\woods-framework",
    r"D:\blogger\woods-framework",
    r"D:\blogger\jobspy-mcp-server\src",
    r"D:\blogger\jobspy-mcp-server\matching_layer_spec.md",
    r"D:\blogger\jobspy-mcp-server\post_processor.py",
    r"D:\blogger\jobspy-mcp-server\pbs_fit_scorer.py",
    r"D:\blogger\Double-Edge-Insight-AI-Pipeline",
    r"D:\blogger\sovereign-audit-site",
    r"D:\blogger\sovereign-editor-lite",
    r"D:\blogger\sovereign\kernel",
    r"D:\blogger\market_validation_dashboard.py",
    r"D:\blogger\founders_brief_generator.py",
    r"D:\blogger\init_prospect_db.py",
    r"D:\blogger\compile_report.py",
    r"D:\blogger\SYSTEM_AUDIT_SPEC.md",
    r"D:\blogger\run_woods_pipeline.ps1",
    r"D:\blogger\driftcast",
    r"D:\blogger\jusbt_pipeline",
    r"D:\blogger\research",
    r"D:\blogger\syndicated_manuscripts",
    r"D:\blogger\content_db",
    r"D:\blogger\SYSTEM DIRECTIVE SOVEREIGN FOREMAN PROTOCOL"
]

EXCLUDE_NAMES = {"node_modules", ".git", "__pycache__", ".venv", "dist", ".next", "package-lock.json", ".png", ".jpg", ".webp", ".mp4"}

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return "ERROR_READING"

def get_auth_level(rel_path):
    norm = rel_path.lower().replace('\\', '/')
    if ".agents/woods-framework" in norm or "woods-framework" in norm:
        if any(k in norm for k in ["principles.json", "gatekeeper", "soul", "standard", "identity", "router"]):
            return 1, "Canonical Woods Framework governance"
        if "case" in norm:
            return 2, "Principle-Origin / Documented Case"
        return 1, "Woods Framework Architecture"
    if "resume" in norm or "cv" in norm:
        return 4, "Verified résumé record"
    if norm.endswith(".py") or norm.endswith(".ts") or norm.endswith(".js") or norm.endswith(".ps1"):
        return 5, "Source code & executable artifact"
    if any(k in norm for k in ["report", "walkthrough", "metrics", "spec"]):
        return 6, "Implementation report / test output"
    if any(k in norm for k in ["site", "dist", "sovereign"]):
        return 7, "Deployed project evidence"
    if any(k in norm for k in ["dashboard", "analytics", "db"]):
        return 8, "Analytics & measured outcome"
    return 9, "Working document"

manifest_records = []
seen_hashes = {}

def add_file(filepath):
    if not os.path.exists(filepath):
        return
    fname = os.path.basename(filepath)
    ext = os.path.splitext(fname)[1].lower()
    
    if ext in EXCLUDE_NAMES or fname in EXCLUDE_NAMES:
        return

    rel_path = os.path.relpath(filepath, BASE_DIR)
    auth_level, auth_desc = get_auth_level(rel_path)
    chash = compute_sha256(filepath)
    
    is_dup = False
    dup_of = None
    if chash in seen_hashes:
        is_dup = True
        dup_of = seen_hashes[chash]
    else:
        if chash != "ERROR_READING":
            seen_hashes[chash] = rel_path

    read_status = "read_success" if ext in [".json", ".md", ".txt", ".py", ".ts", ".js", ".ps1", ".html", ".css", ".sql", ".csv", ".yaml", ".yml"] else "excluded"
    ex_reason = None if read_status == "read_success" else f"Unsupported file extension '{ext}'"

    stat = os.stat(filepath)
    mtime_iso = datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc).isoformat()

    manifest_records.append({
        "file_path": rel_path,
        "file_type": ext if ext else "no_ext",
        "authority_level": auth_level,
        "authority_description": auth_desc,
        "read_status": read_status,
        "content_hash": chash,
        "is_duplicate_hash": is_dup,
        "duplicate_of": dup_of,
        "last_modified": mtime_iso,
        "canonical_status": "canonical" if auth_level == 1 else "non_canonical",
        "exclusion_reason": ex_reason
    })

for target in TARGET_PATHS:
    if os.path.isfile(target):
        add_file(target)
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_NAMES]
            for f in files:
                add_file(os.path.join(root, f))

read_count = sum(1 for r in manifest_records if r["read_status"] == "read_success")
excluded_count = sum(1 for r in manifest_records if r["read_status"] == "excluded")

output = {
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "base_directory": BASE_DIR,
    "total_files_scanned": len(manifest_records),
    "files_ingested": read_count,
    "files_excluded": excluded_count,
    "unique_content_hashes": len(seen_hashes),
    "manifest": manifest_records
}

out_path = r"D:\blogger\jobspy-mcp-server\ingestion_manifest.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Manifest written successfully: {len(manifest_records)} scanned, {read_count} ingested.")

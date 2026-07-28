import os
import re
import json
import hashlib
import datetime
from typing import Dict, List, Any, Tuple

BASE_DIR = r"D:\blogger"

# Key project directories to scan for evidence
TARGET_DIRS = [
    r"D:\blogger\.agents",
    r"D:\blogger\woods-framework",
    r"D:\blogger\jobspy-mcp-server",
    r"D:\blogger\Double-Edge-Insight-AI-Pipeline",
    r"D:\blogger\sovereign-audit-site",
    r"D:\blogger\sovereign-editor-lite",
    r"D:\blogger\sovereign",
    r"D:\blogger\market_validation_dashboard.py",
    r"D:\blogger\founders_brief_generator.py",
    r"D:\blogger\init_prospect_db.py",
    r"D:\blogger\compile_report.py",
    r"D:\blogger\SYSTEM_AUDIT_SPEC.md",
    r"D:\blogger\run_woods_pipeline.ps1",
    r"D:\blogger\driftcast",
    r"D:\blogger\openmontage",
    r"D:\blogger\jusbt_pipeline",
    r"D:\blogger\research",
    r"D:\blogger\syndicated_manuscripts",
    r"D:\blogger\content_db",
    r"D:\blogger\blog.entries",
    r"D:\blogger\SYSTEM DIRECTIVE SOVEREIGN FOREMAN PROTOCOL"
]

EXCLUDE_DIRS = {"node_modules", ".git", "__pycache__", ".venv", ".chrome-debug-profile", "chrome-debug-profile", "dist", ".next", ".cache"}

def compute_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return "ERROR_READING"

def determine_authority_level(rel_path: str) -> Tuple[int, str]:
    norm = rel_path.lower().replace('\\', '/')
    if ".agents/woods-framework" in norm or "woods-framework" in norm:
        if "principles.json" in norm or "gatekeeper" in norm or "soul" in norm or "standard" in norm:
            return 1, "Canonical Woods Framework governance"
        if "case" in norm:
            return 2, "Principle-Origin / Documented Case"
        return 1, "Woods Framework Architecture"
    
    if "resume" in norm or "cv" in norm:
        return 4, "Verified résumé record"
    
    if norm.endswith(".py") or norm.endswith(".ts") or norm.endswith(".js") or norm.endswith(".ps1"):
        return 5, "Source code & executable artifact"
    
    if "report" in norm or "walkthrough" in norm or "metrics" in norm or "spec" in norm:
        return 6, "Implementation report / test output"
    
    if "site" in norm or "dist" in norm or "sovereign" in norm:
        return 7, "Deployed project evidence"
    
    if "dashboard" in norm or "analytics" in norm or "db" in norm:
        return 8, "Analytics & measured outcome"
    
    return 9, "Working document"

def scan_target(target_path: str, manifest_records: List[Dict[str, Any]], seen_hashes: Dict[str, str]):
    if os.path.isfile(target_path):
        process_file(target_path, manifest_records, seen_hashes)
    elif os.path.isdir(target_path):
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                full_path = os.path.join(root, f)
                process_file(full_path, manifest_records, seen_hashes)

def process_file(full_path: str, manifest_records: List[Dict[str, Any]], seen_hashes: Dict[str, str]):
    try:
        rel_path = os.path.relpath(full_path, BASE_DIR)
    except Exception:
        rel_path = full_path

    f = os.path.basename(full_path)
    ext = os.path.splitext(f)[1].lower()
    
    # Check size - skip binary files larger than 10MB
    stat = os.stat(full_path)
    if stat.st_size > 10 * 1024 * 1024 and ext not in [".json", ".txt", ".md", ".py"]:
        manifest_records.append({
            "file_path": rel_path,
            "file_type": ext if ext else "no_ext",
            "authority_level": 9,
            "authority_description": "Large binary asset",
            "read_status": "excluded",
            "content_hash": "SKIPPED_LARGE_FILE",
            "is_duplicate_hash": False,
            "duplicate_of": None,
            "last_modified": datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc).isoformat(),
            "canonical_status": "non_canonical",
            "exclusion_reason": f"File size ({stat.st_size} bytes) exceeds 10MB limit"
        })
        return

    auth_level, auth_desc = determine_authority_level(rel_path)
    chash = compute_sha256(full_path)
    
    is_dup = False
    dup_of = None
    if chash in seen_hashes:
        is_dup = True
        dup_of = seen_hashes[chash]
    else:
        if chash != "ERROR_READING":
            seen_hashes[chash] = rel_path

    if ext in [".json", ".md", ".txt", ".py", ".ts", ".js", ".ps1", ".html", ".css", ".sql", ".csv", ".yaml", ".yml"]:
        read_status = "read_success"
        exclusion_reason = None
    else:
        read_status = "excluded"
        exclusion_reason = f"Unsupported file extension '{ext}' for semantic text ingestion"

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
        "exclusion_reason": exclusion_reason
    })

def main():
    manifest_records = []
    seen_hashes = {}

    for t in TARGET_DIRS:
        if os.path.exists(t):
            scan_target(t, manifest_records, seen_hashes)

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
    print(f"Ingestion Manifest complete: {len(manifest_records)} scanned, {read_count} ingested, saved to {out_path}.")

if __name__ == "__main__":
    main()

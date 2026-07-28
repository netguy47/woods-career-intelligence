import os
import re
import json
import hashlib
import datetime
from typing import Dict, List, Any, Tuple

BASE_DIR = r"D:\blogger"
WOODS_DIRS = [
    r"D:\blogger\.agents\woods-framework",
    r"D:\blogger\woods-framework"
]

EXCLUDE_PATTERNS = [
    r"^\.env", r"\.pem$", r"\.key$", r"\.pfx$", r"\.crt$", r"secret", r"credential", r"token",
    r"node_modules", r"\.venv", r"^venv$", r"\.git", r"dist", r"build", r"\.next", r"coverage", r"__pycache__",
    r"\.db$", r"\.sqlite$", r"\.zip$", r"\.tar$", r"\.gz$", r"\.exe$", r"\.dll$", r"\.png$", r"\.jpg$", r"\.jpeg$", r"\.webp$", r"\.mp4$", r"\.ico$"
]

def is_excluded_path(rel_path: str, filename: str) -> Tuple[bool, str]:
    norm = rel_path.lower().replace('\\', '/')
    fname = filename.lower()

    if fname.startswith(".env") or "secret" in fname or "token" in fname or fname.endswith((".pem", ".key", ".pfx")):
        return True, "Security/Secret file exclusion policy"

    for p in ["node_modules/", ".venv/", "venv/", ".git/", "dist/", "build/", ".next/", "coverage/", "__pycache__/"]:
        if p in norm:
            return True, f"System/Dependency directory exclusion ({p.rstrip('/')})"

    ext = os.path.splitext(fname)[1]
    if ext in [".db", ".sqlite", ".zip", ".tar", ".gz", ".exe", ".dll", ".png", ".jpg", ".jpeg", ".webp", ".mp4", ".ico", ".pdf"]:
        return True, f"Binary/Media/Database file format exclusion ({ext})"

    return False, ""

def compute_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"ERROR_READING: {str(e)}"

def classify_canonical_status(rel_path: str, filename: str) -> str:
    norm = rel_path.lower().replace('\\', '/')
    fname = filename.lower()

    if "principles.json" in fname:
        return "canonical"
    if "gatekeeper" in fname or "fidelity" in fname or "evidence_to_output" in fname or "post_generation" in fname or "execution_authority" in fname or "pipeline_bridge" in fname:
        return "canonical_supporting"
    if "voluntary_extension_case" in fname or "culture_breakdown_case" in fname or "visibility_case" in fname:
        return "documented_case"
    if "working_case" in fname:
        return "working_case"
    if "candidate" in fname:
        return "candidate"
    if "working_concept" in fname:
        return "working_concept"
    if "deprecated" in fname:
        return "deprecated"
    if "principles/" in norm:
        return "canonical"
    
    return "non_canonical"

def process_phase1_ingestion():
    manifest_records = []
    seen_hashes: Dict[str, str] = {}

    total_scanned = 0
    read_success_cnt = 0
    read_partial_cnt = 0
    parse_failed_cnt = 0
    excluded_cnt = 0
    blocked_cnt = 0
    duplicate_cnt = 0

    for wdir in WOODS_DIRS:
        if not os.path.exists(wdir):
            continue
        for root, dirs, files in os.walk(wdir):
            for f in files:
                total_scanned += 1
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, BASE_DIR)

                is_ex, ex_reason = is_excluded_path(rel_path, f)

                ext = os.path.splitext(f)[1].lower()
                c_status = classify_canonical_status(rel_path, f)

                if is_ex:
                    read_status = "excluded"
                    chash = "NOT_HASHED_EXCLUDED"
                    excluded_cnt += 1
                    is_dup = False
                    dup_of = None
                else:
                    chash = compute_sha256(full_path)
                    if chash in seen_hashes:
                        is_dup = True
                        dup_of = seen_hashes[chash]
                        read_status = "duplicate_content"
                        duplicate_cnt += 1
                    else:
                        is_dup = False
                        dup_of = None
                        if chash.startswith("ERROR_READING"):
                            read_status = "parse_failed"
                            parse_failed_cnt += 1
                        else:
                            seen_hashes[chash] = rel_path
                            read_status = "read_success"
                            read_success_cnt += 1

                stat = os.stat(full_path)
                mtime_iso = datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc).isoformat()

                manifest_records.append({
                    "file_path": rel_path,
                    "file_type": ext if ext else "no_ext",
                    "authority_level": 1 if "agents" in rel_path or "principles" in rel_path else 2,
                    "read_status": read_status,
                    "content_hash": chash,
                    "is_duplicate_hash": is_dup,
                    "duplicate_of": dup_of,
                    "last_modified": mtime_iso,
                    "canonical_status": c_status,
                    "proposed_evidence_records_count": 0,  # Will be calculated during record proposal
                    "exclusion_reason": ex_reason if is_ex else None
                })

    output = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "phase": "Phase 1 - Woods Framework Focus Only",
        "base_directory": BASE_DIR,
        "total_files_scanned": total_scanned,
        "files_read_success": read_success_cnt,
        "files_read_partial": read_partial_cnt,
        "files_parse_failed": parse_failed_cnt,
        "files_excluded": excluded_cnt,
        "files_blocked": blocked_cnt,
        "files_duplicate_content": duplicate_cnt,
        "unique_content_hashes": len(seen_hashes),
        "manifest": manifest_records
    }

    out_path = r"D:\blogger\jobspy-mcp-server\phase1_woods_ingestion_manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Phase 1 Woods Framework Ingestion Manifest complete: {total_scanned} scanned, {read_success_cnt} read, {duplicate_cnt} duplicates.")
    return output

if __name__ == "__main__":
    process_phase1_ingestion()

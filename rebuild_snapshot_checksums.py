import os
import hashlib
import json

PACKAGE_DIR = r"D:\blogger\jobspy-mcp-server\phase2_review_package"

def compute_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def rebuild_checksums():
    files = sorted(os.listdir(PACKAGE_DIR))
    
    checksum_lines = []
    json_checksums = {}

    print("--- Frozen Phase 2 Review Snapshot Checksum Audit ---")
    
    for fname in files:
        if fname in ["checksums.sha256", "checksums.json"]:
            # Self-exclusion rule: Checksum manifest files do not record their own hash within themselves to prevent recursive hash loops.
            continue
        
        fpath = os.path.join(PACKAGE_DIR, fname)
        if os.path.isfile(fpath):
            chash = compute_sha256(fpath)
            json_checksums[fname] = chash
            checksum_lines.append(f"{chash}  {fname}")
            print(f"Verified & Hashed: {fname} -> {chash}")

    # Write checksums.sha256
    sha_path = os.path.join(PACKAGE_DIR, "checksums.sha256")
    with open(sha_path, "w", encoding="utf-8") as f:
        f.write("\n".join(checksum_lines) + "\n")

    # Write checksums.json (contains inventory metadata and self-exclusion documentation)
    json_data = {
        "generated_at": "2026-07-27T15:26:00Z",
        "snapshot_title": "Frozen Phase 2 Review Snapshot",
        "self_exclusion_note": "checksums.sha256 and checksums.json exclude their own hashes to prevent recursive hash instability.",
        "total_non_checksum_artifacts": len(json_checksums),
        "checksums": json_checksums
    }
    
    json_path = os.path.join(PACKAGE_DIR, "checksums.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    print(f"\nSnapshot Checksums successfully updated across {len(json_checksums)} artifacts.")

if __name__ == "__main__":
    rebuild_checksums()

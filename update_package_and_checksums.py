import os
import shutil
import hashlib
import json

SRC_DIR = r"D:\blogger\jobspy-mcp-server"
PKG_DIR = r"D:\blogger\jobspy-mcp-server\phase2_review_package"

FILES_TO_SYNC = [
    "career_evidence_registry.json",
    "professional_identity_model.json",
    "project_evidence_dossiers.md",
    "woods_professional_capability_map.md",
    "ingestion_completeness_report.md",
    "linkedin_profile_gap_analysis.md",
    "top_10_bias_audit.md",
    "phase2_execution_log.md",
    "phase2_correction_report.md",
    "pbs_fit_scorer.py",
    "pbs_fit_scorer_pre_career_direction.py",
    "test_pbs_fit_scorer.py",
    "scorer_revision_plan.md",
    "scorer_weight_validation.json",
    "scorer_schema_example.json",
    "scorer_unit_test_results.json",
    "scorer_change_log.md"
]

def compute_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def sync_and_checksum():
    for f in FILES_TO_SYNC:
        src = os.path.join(SRC_DIR, f)
        dst = os.path.join(PKG_DIR, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Synced to package: {f}")

    # Rebuild checksums
    all_files = sorted(os.listdir(PKG_DIR))
    checksum_lines = []
    json_checksums = {}

    print("\n--- Rebuilding Snapshot Checksum Inventory ---")
    for fname in all_files:
        if fname in ["checksums.sha256", "checksums.json"]:
            continue
        
        fpath = os.path.join(PKG_DIR, fname)
        if os.path.isfile(fpath):
            chash = compute_sha256(fpath)
            json_checksums[fname] = chash
            checksum_lines.append(f"{chash}  {fname}")
            print(f"Checksum OK: {fname} -> {chash}")

    # Write checksums.sha256
    sha_manifest = os.path.join(PKG_DIR, "checksums.sha256")
    with open(sha_manifest, "w", encoding="utf-8") as f:
        f.write("\n".join(checksum_lines) + "\n")

    # Write checksums.json
    json_data = {
        "generated_at": "2026-07-27T16:28:00Z",
        "snapshot_title": "Frozen Phase 2 Review Snapshot (Full Code & Scorer Audited)",
        "self_exclusion_note": "checksums.sha256 and checksums.json exclude their own hashes from their internal lists to prevent recursive hash instability.",
        "total_non_checksum_artifacts": len(json_checksums),
        "checksums": json_checksums
    }
    
    json_path = os.path.join(PKG_DIR, "checksums.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    print(f"\nChecksum inventory successfully built across {len(json_checksums)} non-checksum artifacts.")

if __name__ == "__main__":
    sync_and_checksum()

import os
import shutil
import hashlib
import json

SOURCE_DIR = r"D:\blogger\jobspy-mcp-server"
PACKAGE_DIR = r"D:\blogger\jobspy-mcp-server\phase2_review_package"

FILES_TO_COPY = [
    ("career_evidence_registry.json", "career_evidence_registry.json"),
    ("ingestion_completeness_report.md", "ingestion_completeness_report.md"),
    ("project_evidence_dossiers.md", "project_evidence_dossiers.md"),
    ("woods_professional_capability_map.md", "woods_professional_capability_map.md"),
    ("professional_identity_model.json", "professional_identity_model.json"),
    ("linkedin_profile_gap_analysis.md", "linkedin_profile_gap_analysis.md"),
    ("top_10_bias_audit.md", "top_10_bias_audit.md"),
    ("ingestion_manifest.json", "phase2_ingestion_manifest.json"),
    ("phase2_execution_log.md", "phase2_execution_log.md")
]

def compute_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def create_review_package():
    if os.path.exists(PACKAGE_DIR):
        shutil.rmtree(PACKAGE_DIR)
    os.makedirs(PACKAGE_DIR, exist_ok=True)

    checksums = {}
    checksum_lines = []

    for src_name, dst_name in FILES_TO_COPY:
        src_path = os.path.join(SOURCE_DIR, src_name)
        dst_path = os.path.join(PACKAGE_DIR, dst_name)

        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            h = compute_sha256(dst_path)
            checksums[dst_name] = h
            checksum_lines.append(f"{h}  {dst_name}")
            print(f"Copied & Hashed: {dst_name} -> {h}")
        else:
            print(f"WARNING: Source file not found: {src_path}")

    # Write checksum files
    sha_file = os.path.join(PACKAGE_DIR, "checksums.sha256")
    with open(sha_file, "w", encoding="utf-8") as f:
        f.write("\n".join(checksum_lines) + "\n")

    json_sha_file = os.path.join(PACKAGE_DIR, "checksums.json")
    with open(json_sha_file, "w", encoding="utf-8") as f:
        json.dump({"generated_at": "2026-07-27T15:24:00Z", "checksums": checksums}, f, indent=2)

    print(f"\nPhase 2 Review Package successfully assembled at:\n{PACKAGE_DIR}")

if __name__ == "__main__":
    create_review_package()

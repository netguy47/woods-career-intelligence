import os
import zipfile
import hashlib

SOURCE_DIR = r"D:\blogger\jobspy-mcp-server\phase2_review_package"
ZIP_OUTPUT_PATH = r"D:\blogger\jobspy-mcp-server\woods_career_intelligence_phase2_frozen_snapshot.zip"

FILES_TO_PACK = [
    "career_evidence_registry.json",
    "professional_identity_model.json",
    "project_evidence_dossiers.md",
    "woods_professional_capability_map.md",
    "ingestion_completeness_report.md",
    "linkedin_profile_gap_analysis.md",
    "top_10_bias_audit.md",
    "genuine_phase2_ingestion_manifest.json",
    "phase1_manifest_incorrectly_packaged_as_phase2.json",
    "phase2_execution_log.md",
    "phase2_correction_report.md",
    "pbs_fit_scorer.py",
    "pbs_fit_scorer_pre_career_direction.py",
    "test_pbs_fit_scorer.py",
    "scorer_revision_plan.md",
    "scorer_weight_validation.json",
    "scorer_schema_example.json",
    "scorer_unit_test_results.json",
    "scorer_change_log.md",
    "checksums.sha256",
    "checksums.json"
]

def create_zip_archive():
    missing_files = [
        fname
        for fname in FILES_TO_PACK
        if not os.path.isfile(os.path.join(SOURCE_DIR, fname))
    ]

    if missing_files:
        raise FileNotFoundError(
            "Archive not created. Missing required files:\n- "
            + "\n- ".join(missing_files)
        )

    temp_zip_path = ZIP_OUTPUT_PATH + ".tmp"

    if os.path.exists(temp_zip_path):
        os.remove(temp_zip_path)

    fixed_time = (2026, 7, 27, 16, 28, 0)

    with zipfile.ZipFile(
        temp_zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zipf:
        for fname in FILES_TO_PACK:
            fpath = os.path.join(SOURCE_DIR, fname)
            with open(fpath, "rb") as f:
                data = f.read()
            zinfo = zipfile.ZipInfo(filename=fname, date_time=fixed_time)
            zinfo.compress_type = zipfile.ZIP_DEFLATED
            zipf.writestr(zinfo, data)
            print(f"Added to ZIP: {fname}")

    # Verify exact archive inventory before replacing the final ZIP.
    with zipfile.ZipFile(temp_zip_path, "r") as zipf:
        archived_files = zipf.namelist()

    if archived_files != FILES_TO_PACK:
        os.remove(temp_zip_path)
        raise RuntimeError(
            "Archive inventory does not match the required file list."
        )

    os.replace(temp_zip_path, ZIP_OUTPUT_PATH)

    sha256 = hashlib.sha256()
    with open(ZIP_OUTPUT_PATH, "rb") as archive:
        for chunk in iter(lambda: archive.read(65536), b""):
            sha256.update(chunk)

    zip_hash = sha256.hexdigest()
    zip_size = os.path.getsize(ZIP_OUTPUT_PATH)

    print("\n========================================================")
    print(f"Full Snapshot Archive Created: {ZIP_OUTPUT_PATH}")
    print(f"Archive Size: {zip_size:,} bytes")
    print(f"Final Archive SHA-256: {zip_hash}")
    print("========================================================")

if __name__ == "__main__":
    create_zip_archive()

import hashlib
import json
import os
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SRC_DIR = Path(r"D:\blogger\jobspy-mcp-server")
PKG_DIR = SRC_DIR / "scorer_code_review_package"
ZIP_OUTPUT_PATH = SRC_DIR / "woods_career_intelligence_scorer_code_review.zip"

FILES_TO_SYNC = [
    "pbs_fit_scorer.py",
    "pbs_fit_scorer_pre_career_direction.py",
    "test_pbs_fit_scorer.py",
    "calibration_runner.py",
    "recommendation_policy.md",
    "evidence_matching_spec.md",
    "matcher_calibration_report.md",
    "scorer_revision_plan.md",
    "scorer_weight_validation.json",
    "scorer_schema_example.json",
    "calibration_relevance_labels.json",
    "evaluative_calibration_results.json",
    "evaluative_holdout_results.json",
    "execution_derived_threshold_metrics.json",
    "report_integrity_test_results.json",
    "score_separation_test_results.json",
    "scorer_change_log.md",
    "career_evidence_registry.json",
    "professional_identity_model.json",
]

CHECKSUM_FILES = {
    "checksums.sha256",
    "checksums.json",
}


def compute_sha256(filepath: Path) -> str:
    sha256 = hashlib.sha256()

    with filepath.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def validate_source_files() -> None:
    missing = [
        filename
        for filename in FILES_TO_SYNC
        if not (SRC_DIR / filename).is_file()
    ]

    if missing:
        raise FileNotFoundError(
            "Review package was not created. Missing required files:\n- "
            + "\n- ".join(missing)
        )


def reset_package_directory() -> None:
    if PKG_DIR.exists():
        shutil.rmtree(PKG_DIR)

    PKG_DIR.mkdir(parents=True, exist_ok=False)


def sync_files() -> None:
    for filename in FILES_TO_SYNC:
        source = SRC_DIR / filename
        destination = PKG_DIR / filename

        shutil.copy2(source, destination)
        print(f"Synced: {filename}")


def build_checksum_inventory() -> dict[str, str]:
    checksums: dict[str, str] = {}

    for filename in FILES_TO_SYNC:
        filepath = PKG_DIR / filename
        checksums[filename] = compute_sha256(filepath)
        print(f"Checksum: {filename} -> {checksums[filename]}")

    return checksums


def write_checksum_files(checksums: dict[str, str]) -> None:
    sha_manifest = PKG_DIR / "checksums.sha256"
    json_manifest = PKG_DIR / "checksums.json"

    sha_lines = [
        f"{checksums[filename]}  {filename}"
        for filename in FILES_TO_SYNC
    ]

    sha_manifest.write_text(
        "\n".join(sha_lines) + "\n",
        encoding="utf-8",
    )

    json_data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_title": (
            "PBS Scorer Code Review Package — Revision 4.3 Evaluative Calibration & Policy Engine Hardening"
        ),
        "package_status": "Implemented, execution-tested, pending independent approval",
        "self_exclusion_note": (
            "checksums.sha256 and checksums.json exclude their own hashes "
            "to avoid recursive checksum instability."
        ),
        "total_non_checksum_artifacts": len(checksums),
        "expected_files": FILES_TO_SYNC,
        "checksums": checksums,
    }

    json_manifest.write_text(
        json.dumps(json_data, indent=2),
        encoding="utf-8",
    )


def verify_package(checksums: dict[str, str]) -> None:
    actual_files = {
        path.name
        for path in PKG_DIR.iterdir()
        if path.is_file()
    }

    expected_files = set(FILES_TO_SYNC) | CHECKSUM_FILES

    if actual_files != expected_files:
        missing = sorted(expected_files - actual_files)
        unexpected = sorted(actual_files - expected_files)

        raise RuntimeError(
            "Package inventory verification failed.\n"
            f"Missing: {missing}\n"
            f"Unexpected: {unexpected}"
        )

    mismatches = []

    for filename, expected_hash in checksums.items():
        actual_hash = compute_sha256(PKG_DIR / filename)

        if actual_hash != expected_hash:
            mismatches.append(filename)

    if mismatches:
        raise RuntimeError(
            "Checksum verification failed for:\n- "
            + "\n- ".join(mismatches)
        )


def build_zip_archive() -> str:
    temp_zip_path = Path(str(ZIP_OUTPUT_PATH) + ".tmp")
    if temp_zip_path.exists():
        temp_zip_path.unlink()

    fixed_time = (2026, 7, 27, 21, 15, 0)
    all_files_to_pack = FILES_TO_SYNC + ["checksums.sha256", "checksums.json"]

    with zipfile.ZipFile(temp_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for fname in all_files_to_pack:
            fpath = PKG_DIR / fname
            data = fpath.read_bytes()
            zinfo = zipfile.ZipInfo(filename=fname, date_time=fixed_time)
            zinfo.compress_type = zipfile.ZIP_DEFLATED
            zipf.writestr(zinfo, data)

    temp_zip_path.replace(ZIP_OUTPUT_PATH)
    zip_hash = compute_sha256(ZIP_OUTPUT_PATH)
    return zip_hash


def main() -> None:
    validate_source_files()
    reset_package_directory()
    sync_files()

    checksums = build_checksum_inventory()
    write_checksum_files(checksums)
    verify_package(checksums)
    zip_hash = build_zip_archive()

    print("\n========================================================")
    print(f"Review package created: {PKG_DIR}")
    print(f"Substantive files: {len(FILES_TO_SYNC)}")
    print(f"Total files including checksum manifests: {len(FILES_TO_SYNC) + 2}")
    print("Inventory and checksum verification: PASSED")
    print(f"ZIP Archive Created: {ZIP_OUTPUT_PATH}")
    print(f"ZIP SHA-256 Checksum: {zip_hash}")
    print("========================================================")


if __name__ == "__main__":
    main()

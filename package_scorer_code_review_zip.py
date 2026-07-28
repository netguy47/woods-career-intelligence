import hashlib
import os
import zipfile
from pathlib import Path

PKG_DIR = Path(
    r"D:\blogger\jobspy-mcp-server\scorer_code_review_package"
)

ZIP_PATH = Path(
    r"D:\blogger\jobspy-mcp-server"
    r"\woods_career_intelligence_scorer_code_review.zip"
)


def compute_sha256(filepath: Path) -> str:
    sha256 = hashlib.sha256()

    with filepath.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_zip() -> None:
    temp_zip = ZIP_PATH.with_suffix(".zip.tmp")

    if temp_zip.exists():
        temp_zip.unlink()

    expected_files = sorted(
        path.name
        for path in PKG_DIR.iterdir()
        if path.is_file()
    )

    if not expected_files:
        raise RuntimeError("The scorer review package is empty.")

    with zipfile.ZipFile(
        temp_zip,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for filename in expected_files:
            archive.write(
                PKG_DIR / filename,
                arcname=filename,
            )

    with zipfile.ZipFile(temp_zip, "r") as archive:
        archived_files = sorted(archive.namelist())
        bad_files = archive.testzip()

    if archived_files != expected_files:
        temp_zip.unlink(missing_ok=True)
        raise RuntimeError("ZIP inventory does not match the package.")

    if bad_files is not None:
        temp_zip.unlink(missing_ok=True)
        raise RuntimeError(f"Corrupt ZIP entry detected: {bad_files}")

    os.replace(temp_zip, ZIP_PATH)

    print(f"Archive: {ZIP_PATH}")
    print(f"Size: {ZIP_PATH.stat().st_size:,} bytes")
    print(f"SHA-256: {compute_sha256(ZIP_PATH)}")


if __name__ == "__main__":
    create_zip()

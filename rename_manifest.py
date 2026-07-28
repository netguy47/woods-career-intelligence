import os

pkg_dir = r"D:\blogger\jobspy-mcp-server\phase2_review_package"
old_file = os.path.join(pkg_dir, "phase2_ingestion_manifest.json")
new_file = os.path.join(pkg_dir, "phase1_manifest_incorrectly_packaged_as_phase2.json")

if os.path.exists(old_file):
    os.rename(old_file, new_file)
    print(f"Renamed: {old_file} -> {new_file}")
else:
    print(f"File not found: {old_file}")

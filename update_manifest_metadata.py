import json
import os

manifest_path = r"D:\blogger\jobspy-mcp-server\phase2_review_package\genuine_phase2_ingestion_manifest.json"

with open(manifest_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Add required metadata fields
data["manifest_type"] = "reconstructed_phase2_provenance_manifest"
data["created_after_execution"] = True
data["direct_read_provenance_available"] = "mixed"
data["confidence_model"] = "per_record"

# Ensure title clearly states documented artifacts, not successfully ingested files
data["documentation_note"] = "3,159 total artifacts documented across workspace discovery; contains a mix of reconstructed provenance records and unverified scan entries."

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Updated genuine_phase2_ingestion_manifest.json header metadata.")

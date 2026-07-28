import json
import os

REGISTRY_PATH = r"D:\blogger\jobspy-mcp-server\career_evidence_registry.json"

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

records = data.get("evidence_records", [])
print(f"Current raw record count: {len(records)}")

# Let's inspect unique domains
domains = sorted(list(set([r["capability_domain"] for r in records])))
print(f"Current unique capability domains ({len(domains)}):")
for d in domains:
    print(f" - {d}")

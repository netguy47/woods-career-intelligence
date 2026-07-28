import hashlib
import json
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestPBSProtectedFiles(unittest.TestCase):
    def test_protected_hashes_match_assurance_state(self):
        state = json.loads((BASE_DIR / "pbs_assurance_state.json").read_text(encoding="utf-8"))
        protected_files = state.get("protected_files", [])
        if not protected_files:
            protected_files = [
                {"path": filename, "sha256": expected_hash}
                for filename, expected_hash in state["protected_inputs"].items()
            ]
        for item in protected_files:
            filename = item["path"]
            self.assertEqual(sha256(BASE_DIR / filename), item["sha256"], filename)

    def test_policy_inputs_are_present(self):
        self.assertTrue((BASE_DIR / "recommendation_policy.md").is_file())
        self.assertTrue((BASE_DIR / "professional_identity_model.json").is_file())


if __name__ == "__main__":
    unittest.main()

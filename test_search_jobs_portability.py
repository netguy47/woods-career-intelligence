import unittest
from pathlib import Path


SOURCE = (Path(__file__).parent / "src" / "tools" / "search-jobs.js").read_text(encoding="utf-8")


class TestSearchJobsPortability(unittest.TestCase):
    def test_uses_portable_resolution_and_non_shell_arguments(self):
        self.assertNotIn("D:\\blogger", SOURCE)
        self.assertNotIn("D:/blogger", SOURCE)
        self.assertIn("PYTHON_CMD", SOURCE)
        self.assertIn("JOBSPY_MAIN_PATH", SOURCE)
        self.assertIn("DOCKER_CMD", SOURCE)
        self.assertIn("JOBSPY_DOCKER_IMAGE", SOURCE)
        self.assertIn("spawnSync", SOURCE)
        self.assertIn("commandArgs", SOURCE)


if __name__ == "__main__":
    unittest.main()

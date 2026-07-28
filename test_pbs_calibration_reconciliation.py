import json
import unittest
from pathlib import Path

from calibration_runner import CALIBRATION_JOBS, HOLDOUT_JOBS, LABELS_FILE_PATH
from pbs_fit_scorer import evaluate_job


BASE_DIR = Path(__file__).parent


class TestPBSCalibrationReconciliation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with LABELS_FILE_PATH.open("r", encoding="utf-8") as handle:
            cls.labels = json.load(handle)["case_labels"]
        cls.jobs = {job["case_id"]: job for job in CALIBRATION_JOBS + HOLDOUT_JOBS}

    def test_ground_truth_labels_are_unchanged_and_failures_are_policy_inconsistent(self):
        expected_failures = {
            "calib-01": (46.3, "Priority Application", "Do Not Prioritize"),
            "calib-02": (27.2, "Consider Application", "Do Not Prioritize"),
            "calib-03": (33.4, "Priority Application", "Do Not Prioritize"),
            "calib-04": (34.2, "Priority Application", "Do Not Prioritize"),
            "calib-05": (44.1, "Priority Application", "Do Not Prioritize"),
            "holdout-01": (44.3, "Consider Application", "Do Not Prioritize"),
        }

        for case_id, (expected_score, expected_recommendation, actual_recommendation) in expected_failures.items():
            output = evaluate_job(self.jobs[case_id])
            label = self.labels[case_id]
            self.assertEqual(label["expected_fit_recommendation"], expected_recommendation)
            self.assertEqual(output["fit_recommendation"], actual_recommendation)
            self.assertEqual(output["pbs_job_fit_score_pre_calibration"], expected_score)
            self.assertLess(output["pbs_job_fit_score_pre_calibration"], 50.0)
            self.assertEqual(output["recommendation_policy_trace"]["pbs_threshold_pass"], False)

    def test_calibration_and_holdout_sets_remain_disjoint(self):
        calibration_ids = {job["case_id"] for job in CALIBRATION_JOBS}
        holdout_ids = {job["case_id"] for job in HOLDOUT_JOBS}
        self.assertTrue(calibration_ids.isdisjoint(holdout_ids))


if __name__ == "__main__":
    unittest.main()

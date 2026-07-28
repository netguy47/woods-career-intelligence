import unittest

from pbs_fit_scorer import determine_fit_recommendation_and_policy_trace


class TestPBSBoundaries(unittest.TestCase):
    CONTEXT = {
        "confidence_score": 0.50,
        "confidence_level": "Moderate",
        "dimension_coverage": {"d2_active": True, "d3_active": True},
    }

    def recommend(self, eligibility, score):
        return determine_fit_recommendation_and_policy_trace(
            eligibility,
            score,
            "Lane_A",
            0.80,
            0.85,
            self.CONTEXT,
            [],
            [],
            False,
        )[0]

    def test_policy_boundaries(self):
        self.assertEqual(self.recommend(True, 49.99), "Do Not Prioritize")
        self.assertEqual(self.recommend(True, 50.00), "Consider Application")
        self.assertEqual(self.recommend(True, 64.99), "Consider Application")
        self.assertEqual(self.recommend(True, 65.00), "Priority Application")

    def test_unresolved_eligibility_requires_manual_review(self):
        self.assertEqual(self.recommend(None, 65.00), "Manual Review")


if __name__ == "__main__":
    unittest.main()

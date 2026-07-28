import unittest

from pbs_fit_scorer import evaluate_job


class TestPBSAdversarialCases(unittest.TestCase):
    def test_required_license_is_hard_ineligible_gate(self):
        result = evaluate_job({
            "title": "Healthcare Quality Auditor",
            "location": "Remote",
            "is_remote": True,
            "description": "Perform clinical pharmacy quality audits. Active Registered Pharmacist (PharmD) license required.",
        })
        self.assertFalse(result["eligibility_disposition"])
        self.assertEqual(result["fit_recommendation"], "Do Not Apply — Ineligible")

    def test_unresolved_location_requires_manual_review(self):
        result = evaluate_job({
            "title": "Operations Manager",
            "location": "St. Louis, MO",
            "description": "Lead multi-unit store operations, labor scheduling, manager mentorship, and operational improvement.",
        })
        self.assertIsNone(result["eligibility_disposition"])
        self.assertEqual(result["fit_recommendation"], "Manual Review")

    def test_preferred_degree_is_not_confused_with_scrum_master(self):
        result = evaluate_job({
            "title": "Technical Project Manager",
            "location": "Remote",
            "is_remote": True,
            "description": "Lead software development sprints as a Scrum Master. Master's degree preferred.",
        })
        preferred = [item for item in result["requirement_details"] if item.get("requirement_level") == "preferred"]
        self.assertEqual(len(preferred), 1)
        self.assertEqual(preferred[0]["state"], "preferred_gap")

    def test_unverified_provenance_is_not_cited(self):
        result = evaluate_job(
            {
                "title": "Workflow Automation Specialist",
                "location": "Remote",
                "is_remote": True,
                "description": "Design workflow automation and operational telemetry dashboards.",
            },
            evidence_registry=[{
                "evidence_id": "EV-TEST-001",
                "specific_capability": "workflow automation",
                "evidence_strength": "provenance_unverified",
                "provenance_unverified": True,
            }],
        )
        self.assertEqual(result["evidence_citations"], [])

    def test_unknown_role_and_empty_description_are_safe(self):
        unknown = evaluate_job({
            "title": "Particle Physics Research Scientist",
            "location": "Remote",
            "is_remote": True,
            "description": "Calibrate particle accelerator detectors and publish theoretical physics research.",
        })
        empty = evaluate_job({"title": "Operations Manager"})
        self.assertEqual(unknown["fit_recommendation"], "Do Not Prioritize")
        self.assertEqual(unknown["strategic_value"], "Insufficient Information")
        self.assertEqual(empty["fit_recommendation"], "Manual Review")

    def test_identical_inputs_are_deterministic(self):
        job = {
            "title": "District Manager",
            "location": "St. Louis, MO",
            "post_processing": {"location_status": "within_range"},
            "description": "Lead multi-unit restaurant operations, P&L, labor scheduling, and inventory management.",
        }
        self.assertEqual(evaluate_job(job), evaluate_job(job))


if __name__ == "__main__":
    unittest.main()

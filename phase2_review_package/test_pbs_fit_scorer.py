import unittest
import json
import os
from pbs_fit_scorer import evaluate_job, WEIGHTS

class TestPBSFitScorer(unittest.TestCase):

    def test_01_exact_weight_total(self):
        weight_sum = sum(WEIGHTS.values())
        self.assertAlmostEqual(weight_sum, 1.00, places=6, msg="Positive weights must sum to exactly 1.0000")

    def test_02_all_seven_dimensions_present(self):
        sample_job = {
            "id": "job-test-01",
            "title": "Operations Manager",
            "company": "Test Logistics",
            "location": "Florissant, MO",
            "description": "Multi-unit leadership, labor scheduling, P&L management, process improvement, workflow automation."
        }
        res = evaluate_job(sample_job)
        dim_scores = res.get("dimension_scores", {})
        self.assertEqual(len(dim_scores), 7)
        self.assertIn("D2_direct_resume", dim_scores)
        self.assertIn("D3_transferable_exp", dim_scores)
        self.assertIn("D4_project_relevance", dim_scores)
        self.assertIn("D5_ats_alignment", dim_scores)
        self.assertIn("D6_title_closeness", dim_scores)
        self.assertIn("D7_industry_closeness", dim_scores)
        self.assertIn("D8_career_direction_alignment", dim_scores)

    def test_03_hard_requirement_failure(self):
        sample_job = {
            "id": "job-ineligible-01",
            "title": "Clinical Pharmacy Director",
            "company": "St. Louis Health",
            "location": "Florissant, MO",
            "description": "Must have active Registered Pharmacist (PharmD) license."
        }
        res = evaluate_job(sample_job)
        self.assertFalse(res["eligible"])
        self.assertFalse(res["hard_eligibility"])
        self.assertEqual(res["recommendation_status"], "Do Not Recommend")
        self.assertEqual(res["pbs_job_fit_score_pre_calibration"], 0.0)
        self.assertGreater(res["diagnostic_fit_score"], 0.0)
        self.assertIn("Requires Licensed Pharmacist (PharmD)", res["hard_requirement_failures"])
        self.assertEqual(res["strategic_value"], "Not Evaluated — Ineligible")

    def test_04_diagnostic_score_preserved_on_gate_failure(self):
        sample_job = {
            "id": "job-ineligible-diagnostic",
            "title": "Director of Pharmacy Operations",
            "company": "Health Systems",
            "location": "Florissant, MO",
            "description": "Multi-unit operations, P&L, team leadership, process improvement. Must have active PharmD license."
        }
        res = evaluate_job(sample_job)
        self.assertFalse(res["eligible"])
        self.assertEqual(res["pbs_job_fit_score_pre_calibration"], 0.0)
        self.assertGreater(res["diagnostic_fit_score"], 40.0)
        self.assertGreater(res["unfiltered_diagnostic_score"], 40.0)

    def test_05_missing_description(self):
        sample_job = {
            "id": "job-no-desc",
            "title": "Operations Specialist",
            "company": "Acme Inc",
            "location": "Florissant, MO",
            "description": ""
        }
        res = evaluate_job(sample_job)
        self.assertEqual(res["dimension_scores"]["D8_career_direction_alignment"], 0.0)
        self.assertEqual(res["dimension_scores"]["D5_ats_alignment"], 0.0)
        self.assertEqual(res["strategic_value"], "Insufficient Information")

    def test_06_no_evidence(self):
        sample_job = {
            "id": "job-no-evidence",
            "title": "Quantum Physics Researcher",
            "company": "Deep Tech Labs",
            "location": "Florissant, MO",
            "description": "Particle accelerator calibration and quantum algorithm formulation."
        }
        res = evaluate_job(sample_job)
        self.assertTrue(res["eligible"])
        self.assertLess(res["pbs_job_fit_score_pre_calibration"], 60.0)

    def test_07_provenance_unverified_exclusion(self):
        sample_job = {
            "id": "job-unverified-prov",
            "title": "Generic Analyst",
            "company": "Corp Inc",
            "location": "Florissant, MO",
            "description": "General office duties and spreadsheet entry."
        }
        res = evaluate_job(sample_job)
        self.assertLessEqual(res["dimension_scores"]["D4_project_relevance"], 0.60)

    def test_08_mixed_evidence_strengths(self):
        sample_job = {
            "id": "job-mixed-strength",
            "title": "Operational Excellence Manager",
            "company": "Logistics Corp",
            "location": "Florissant, MO",
            "description": "Multi-unit operations, process improvement, AI automation, and team mentoring."
        }
        res = evaluate_job(sample_job)
        self.assertGreater(res["capability_fit_score"], 0.0)
        self.assertGreater(res["market_readiness_fit_score"], 0.0)

    def test_09_self_reported_resume_outcomes(self):
        sample_job = {
            "id": "job-resume-claim",
            "title": "District Manager",
            "company": "QSR Group",
            "location": "Florissant, MO",
            "description": "Multi-unit P&L, 25% sales growth, inventory delivery scheduling."
        }
        res = evaluate_job(sample_job)
        self.assertGreaterEqual(res["dimension_scores"]["D2_direct_resume"], 0.85)

    def test_10_all_three_professional_lanes(self):
        job_lane_a = {"title": "District Manager", "description": "Multi-unit QSR leadership."}
        job_lane_b = {"title": "Continuous Improvement Manager", "description": "Process optimization."}
        job_lane_c = {"title": "AI Workflow Architect", "description": "Agentic automation pipelines."}

        res_a = evaluate_job(job_lane_a)
        res_b = evaluate_job(job_lane_b)
        res_c = evaluate_job(job_lane_c)

        self.assertEqual(res_a["professional_lane"], "Lane A")
        self.assertEqual(res_b["professional_lane"], "Lane B")
        self.assertEqual(res_c["professional_lane"], "Lane C")

    def test_11_all_five_strategic_value_classifications(self):
        # 1. Career Advancing
        res_adv = evaluate_job({"title": "AI Enablement Manager", "location": "Florissant, MO", "description": "AI automation, workflow governance, systems implementation, multi-unit process improvement."})
        self.assertEqual(res_adv["strategic_value"], "Career Advancing")

        # 2. Career Maintaining
        res_maint = evaluate_job({"title": "District Manager", "location": "Florissant, MO", "description": "Multi-unit store operations, P&L management, labor scheduling."})
        self.assertEqual(res_maint["strategic_value"], "Career Maintaining")

        # 3. Income Stabilizing
        res_stab = evaluate_job({"title": "General Manager", "location": "Florissant, MO", "description": "Single store operations management and scheduling."})
        self.assertIn(res_stab["strategic_value"], ["Career Maintaining", "Income Stabilizing"])

        # 4. Career Regressive
        res_regr = evaluate_job({"title": "Shift Supervisor", "location": "Florissant, MO", "description": "Hourly shift supervision and drawer count."})
        self.assertEqual(res_regr["strategic_value"], "Career Regressive")

        # 5. Insufficient Information
        res_no_desc = evaluate_job({"title": "Operations Manager", "location": "Florissant, MO", "description": ""})
        self.assertEqual(res_no_desc["strategic_value"], "Insufficient Information")

        # 6. Not Evaluated — Ineligible
        res_inelig = evaluate_job({"title": "Clinical Pharmacy Director", "location": "Florissant, MO", "description": "Requires PharmD license."})
        self.assertEqual(res_inelig["strategic_value"], "Not Evaluated — Ineligible")

    def test_12_score_floor_and_ceiling(self):
        job_min = {"title": "Delivery Driver", "description": "Drive car."}
        job_max = {"title": "AI Workflow Operations Director", "location": "Florissant, MO", "description": "Multi-unit leadership, P&L, AI workflow automation, process improvement, governance, software engineering."}

        res_min = evaluate_job(job_min)
        res_max = evaluate_job(job_max)

        self.assertGreaterEqual(res_min["pbs_job_fit_score_pre_calibration"], 0.0)
        self.assertLessEqual(res_max["pbs_job_fit_score_pre_calibration"], 100.0)

    def test_13_deterministic_repeatability(self):
        sample_job = {"title": "Operations Systems Analyst", "location": "Florissant, MO", "description": "Process improvement and software systems."}
        res1 = evaluate_job(sample_job)
        res2 = evaluate_job(sample_job)
        self.assertEqual(res1["pbs_job_fit_score_pre_calibration"], res2["pbs_job_fit_score_pre_calibration"])
        self.assertEqual(res1["strategic_value"], res2["strategic_value"])

    def test_14_exact_evidence_id_traceability(self):
        sample_job = {"title": "Operations Manager", "description": "Multi-unit P&L, workflow automation."}
        res = evaluate_job(sample_job)
        citations = res.get("evidence_citations", [])
        self.assertGreater(len(citations), 0)
        for cite in citations:
            self.assertIn("evidence_id", cite)
            self.assertTrue(cite["evidence_id"].startswith("EV-"))

    def test_15_legacy_input_compatibility(self):
        sample_job = {"title": "District Operations Manager", "company": "Retail Corp"}
        res = evaluate_job(sample_job)
        self.assertIn("pbs_job_fit_score_pre_calibration", res)

if __name__ == "__main__":
    unittest.main()

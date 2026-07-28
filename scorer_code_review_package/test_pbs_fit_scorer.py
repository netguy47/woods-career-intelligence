import unittest
import json
import copy
import hashlib
from pathlib import Path
from pbs_fit_scorer import evaluate_job, MATCH_THRESHOLDS, WEIGHTS, DEFAULT_IDENTITY_PATH, DEFAULT_REGISTRY_PATH, BASE_DIR

def compute_file_sha256(filepath: Path) -> str:
    if not filepath.is_file():
        return ""
    sha256 = hashlib.sha256()
    with filepath.open("rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def canonicalize(obj):
    if isinstance(obj, float):
        return round(obj, 3)
    elif isinstance(obj, dict):
        return {k: canonicalize(v) for k, v in sorted(obj.items()) if k not in ["execution_timestamp", "runner_version", "scorer_sha256", "registry_sha256", "identity_model_sha256"]}
    elif isinstance(obj, list):
        return [canonicalize(x) for x in obj]
    return obj

class TestPBSFitScorerRevision43(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.initial_identity_hash = compute_file_sha256(DEFAULT_IDENTITY_PATH)
        with DEFAULT_REGISTRY_PATH.open("r", encoding="utf-8") as f:
            cls.registry_data = json.load(f)
        cls.registry_eids = {r["evidence_id"] for r in cls.registry_data["evidence_records"]}

    @classmethod
    def tearDownClass(cls):
        final_hash = compute_file_sha256(DEFAULT_IDENTITY_PATH)
        assert cls.initial_identity_hash == final_hash, "Safeguard Failed: professional_identity_model.json was modified on disk!"

    def test_01_exported_match_thresholds_source_of_truth(self):
        self.assertEqual(MATCH_THRESHOLDS["D2_direct_resume"], 0.35)
        self.assertEqual(MATCH_THRESHOLDS["D3_transferable_exp"], 0.30)
        self.assertEqual(MATCH_THRESHOLDS["D4_project_relevance"], 0.25)

    def test_02_canonicalized_report_integrity_equivalence(self):
        calib_file = BASE_DIR / "evaluative_calibration_results.json"
        self.assertTrue(calib_file.is_file(), "Missing evaluative calibration execution results file")

        from calibration_runner import CALIBRATION_JOBS, HOLDOUT_JOBS
        jobs_map = {j["case_id"]: j for j in CALIBRATION_JOBS + HOLDOUT_JOBS}

        with calib_file.open("r", encoding="utf-8") as f:
            calib_data = json.load(f)

        for case in calib_data["results"]:
            cid = case["case_id"]
            job_input = jobs_map[cid]
            live_out = evaluate_job(job_input)
            rep_out = case["execution_output"]

            c_live = canonicalize(live_out)
            c_rep = canonicalize(rep_out)

            self.assertEqual(c_live["professional_lane"], c_rep["professional_lane"])
            self.assertEqual(c_live["eligibility_disposition"], c_rep["eligibility_disposition"])
            self.assertEqual(c_live["fit_recommendation"], c_rep["fit_recommendation"])
            self.assertEqual(c_live["strategic_value"], c_rep["strategic_value"])
            self.assertEqual(c_live["dimension_scores"], c_rep["dimension_scores"])

    def test_03_score_separation_margins(self):
        # Role 1: Relevant Lane A (District Manager)
        job_district = {
            "title": "District Manager",
            "location": "St. Louis, MO",
            "post_processing": {"location_status": "within_range"},
            "description": "District Manager | Multi-Unit Restaurant Operations Leadership. Oversee store P&L management, general manager mentorship, inventory forecasting, labor scheduling across 5 locations."
        }
        res_district = evaluate_job(job_district)

        # Role 2: Irrelevant Role (Particle Physics)
        job_physics = {
            "title": "Particle Physics Research Scientist",
            "location": "Remote",
            "is_remote": True,
            "description": "Calibrate particle accelerator detectors and solve quantum electrodynamics equations."
        }
        res_physics = evaluate_job(job_physics)

        # Role 3: Misleading Sales Role (AI Sales)
        job_sales = {
            "title": "Commercial AI Sales Director",
            "location": "Remote",
            "is_remote": True,
            "description": "Lead enterprise B2B sales campaigns, manage client account executives, hit revenue quotas for AI software."
        }
        res_sales = evaluate_job(job_sales)

        # Margin Assertions
        district_score = res_district["pbs_job_fit_score_pre_calibration"]
        physics_score = res_physics["pbs_job_fit_score_pre_calibration"]
        sales_score = res_sales["pbs_job_fit_score_pre_calibration"]

        self.assertGreaterEqual(district_score - physics_score, 25.0, "Lane A must score >= 25.0 points above Irrelevant Role")
        self.assertGreaterEqual(district_score - sales_score, 20.0, "Lane A must score >= 20.0 points above Misleading Sales Role")

    def test_04_phrase_independent_degree_extraction(self):
        # Description containing BOTH "Scrum Master" AND "Master's degree preferred"
        job_mixed = {
            "title": "Technical Project Manager",
            "location": "Remote",
            "is_remote": True,
            "description": "Technical Project Manager & Scrum Master leading software development sprints. Master's degree preferred."
        }
        res = evaluate_job(job_mixed)
        pref_reqs = [r for r in res["requirement_details"] if r.get("requirement_level") == "preferred"]
        self.assertEqual(len(pref_reqs), 1)
        self.assertEqual(pref_reqs[0]["state"], "preferred_gap")

    def test_05_unresolved_role_handling(self):
        job_unknown = {
            "title": "Abstract Quantum Strategist",
            "location": "Remote",
            "is_remote": True,
            "description": "Exotic non-standard workflow coordination across complex abstract enterprise environments."
        }
        res = evaluate_job(job_unknown)
        self.assertEqual(res["professional_lane"], "Unresolved")
        self.assertEqual(res["dimension_scores"]["D8_career_direction_alignment"], 0.00)
        self.assertEqual(res["dimension_scores"]["D6_title_closeness"], 0.00)
        self.assertEqual(res["strategic_value"], "Insufficient Information")
        self.assertEqual(res["fit_recommendation"], "Do Not Prioritize")

    def test_06_governed_prefix_routing(self):
        # EV-RES-001 has classification direct -> metadata authoritative
        rec = {"evidence_id": "EV-RES-001", "classification": "direct", "source_type": "résumé", "specific_capability": "District Operations"}
        job_sec = {"all_text": "district operations", "valid_tokens": {"district", "operations"}, "specific_tokens": {"district", "operations"}, "found_phrases": set()}
        
        from pbs_fit_scorer import route_evidence_dimension
        dim, basis, conf, rat = route_evidence_dimension(rec)
        self.assertEqual(dim, "D2_direct_resume")
        self.assertEqual(basis, "metadata_authoritative")
        self.assertEqual(conf, 1.00)

if __name__ == "__main__":
    unittest.main()

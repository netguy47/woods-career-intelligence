import json
from pathlib import Path
from pbs_fit_scorer import evaluate_job, BASE_DIR

FIXTURE_PATH = BASE_DIR / "results_25_job_pbs_trial.json"
CALIB_PATH = BASE_DIR / "evaluative_calibration_results.json"
HOLDOUT_PATH = BASE_DIR / "evaluative_holdout_results.json"

def load_offline_fixtures():
    jobs = []
    
    # 1. Load Calibration & Holdout Jobs with Full Realistic Descriptions
    try:
        from calibration_runner import CALIBRATION_JOBS, HOLDOUT_JOBS
        jobs.extend(CALIBRATION_JOBS)
        jobs.extend(HOLDOUT_JOBS)
    except Exception as e:
        print(f"Note: Could not import CALIBRATION_JOBS/HOLDOUT_JOBS ({e})")

    # 2. Try loading 25-job trial offline fixture
    if FIXTURE_PATH.is_file():
        try:
            with FIXTURE_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("description"):
                            jobs.append(item)
                elif isinstance(data, dict) and "jobs" in data:
                    for item in data["jobs"]:
                        if isinstance(item, dict) and item.get("description"):
                            jobs.append(item)
        except Exception as e:
            print(f"Note: Could not load 25-job trial fixture ({e})")

    return jobs

def run_offline_replay():
    jobs = load_offline_fixtures()
    print(f"Loaded {len(jobs)} offline job fixtures for offline PBS Scorer evaluation.\n")

    results = []
    print(f"{'TITLE':<35} | {'ELIGIBLE':<9} | {'RECOMMENDATION':<24} | {'SCORE':<5} | {'STRATEGIC VALUE':<22}")
    print("-" * 105)

    for job in jobs:
        res = evaluate_job(job)
        results.append(res)
        
        title_str = (res.get("title") or "Unknown Title")[:35]
        elig_str = str(res.get("eligibility_disposition"))
        rec_str = str(res.get("fit_recommendation"))[:24]
        score_val = str(res.get("pbs_job_fit_score_pre_calibration", 0.0))
        strat_str = str(res.get("strategic_value"))[:22]

        print(f"{title_str:<35} | {elig_str:<9} | {rec_str:<24} | {score_val:<5} | {strat_str:<22}")

    out_file = BASE_DIR / "offline_evaluation_results.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump({"total_jobs_evaluated": len(results), "results": results}, f, indent=2)

    print("-" * 105)
    print(f"\nOffline replay complete. Full results saved to: {out_file.name}")

if __name__ == "__main__":
    run_offline_replay()

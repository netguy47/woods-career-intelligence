import json
from pbs_fit_scorer import evaluate_job

def run_single_site_analysis():
    with open("targeted_multisource_matches.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)

    print(f"Re-evaluating {len(jobs)} postings assuming single-site General Manager / Operations Manager focus...")

    single_site_results = []
    for j in jobs:
        title = j.get("title", "")
        company = j.get("company", "")
        loc = j.get("location", "")
        desc = j.get("description", "")
        url = j.get("job_url", "")

        # Evaluate job with broadened title horizon (Operations Manager, General Manager, Process Improvement)
        eval_res = evaluate_job({
            "title": title,
            "company": company,
            "location": loc,
            "description": desc
        })

        # Recalculate title closeness flexibility if General Manager / Operations Manager
        title_lower = title.toLowerCase() if hasattr(title, 'toLowerCase') else title.lower()
        if "general manager" in title_lower or "operations manager" in title_lower or "site manager" in title_lower or "plant manager" in title_lower:
            eval_res["pbs_job_fit_score_pre_calibration"] = min(88.0, eval_res.get("pbs_job_fit_score_pre_calibration", 0.0) + 35.0)
            if eval_res["pbs_job_fit_score_pre_calibration"] >= 65.0:
                eval_res["fit_recommendation"] = "Priority Application"
            elif eval_res["pbs_job_fit_score_pre_calibration"] >= 50.0:
                eval_res["fit_recommendation"] = "Consider Application"

        eval_res["job_url"] = url
        single_site_results.append(eval_res)

    single_site_results.sort(key=lambda x: x.get("pbs_job_fit_score_pre_calibration", 0.0), reverse=True)

    print("\n=== TOP SINGLE-SITE & OPERATIONS MANAGER MATCHES ===")
    for idx, r in enumerate(single_site_results[:10], 1):
        print(f"{idx}. [{r.get('pbs_job_fit_score_pre_calibration'):.1f}%] {r.get('title')} @ {r.get('company')} ({r.get('location')})")
        print(f"   Band: {r.get('fit_recommendation')} | Lane: {r.get('professional_lane')} | URL: {r.get('job_url')}\n")

if __name__ == "__main__":
    run_single_site_analysis()

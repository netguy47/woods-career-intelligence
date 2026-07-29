import json
import pandas as pd
from jobspy import scrape_jobs
from pbs_fit_scorer import evaluate_job

def analyze_indeed_jobs():
    print("Scraping live Indeed listings for 'operations manager OR process improvement manager' near St. Louis, MO...")
    
    try:
        jobs_df = scrape_jobs(
            site_name=["indeed"],
            search_term="operations manager OR process improvement manager",
            location="St. Louis, MO",
            distance=25,
            is_remote=False,
            results_wanted=15,
            hours_old=168,
            country_indeed="USA"
        )
    except Exception as e:
        print(f"JobSpy scrape error: {e}")
        return []

    print(f"Retrieved {len(jobs_df)} raw listings from Indeed. Evaluating through PBS Scorer v4.3...")

    evaluated_results = []
    for idx, row in jobs_df.iterrows():
        title = str(row.get("title", "Untitled"))
        company = str(row.get("company", "Specified Employer"))
        location = str(row.get("location", "St. Louis, MO"))
        description = str(row.get("description", title))
        job_url = str(row.get("job_url", "#"))

        posting = {
            "job_id": f"indeed-{idx+1}",
            "title": title,
            "company": company,
            "location": location,
            "description": description
        }

        eval_res = evaluate_job(posting)
        eval_res["job_url"] = job_url
        eval_res["description"] = description
        evaluated_results.append(eval_res)

    # Sort by PBS Fit Score descending
    evaluated_results.sort(key=lambda x: x.get("pbs_job_fit_score_pre_calibration", 0.0), reverse=True)

    # Save to json file
    with open("indeed_matches_analysis.json", "w", encoding="utf-8") as f:
        json.dump(evaluated_results, f, indent=2)

    print("Saved evaluation output to indeed_matches_analysis.json")
    return evaluated_results

if __name__ == "__main__":
    analyze_indeed_jobs()

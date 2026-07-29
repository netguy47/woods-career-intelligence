import json
from jobspy import scrape_jobs
from pbs_fit_scorer import evaluate_job

def analyze_ziprecruiter_jobs():
    print("Scraping live ZipRecruiter listings for target operations roles near St. Louis / Florissant, MO...")
    
    try:
        jobs_df = scrape_jobs(
            site_name=["zip_recruiter"],
            search_term='operations manager OR district manager OR "process improvement"',
            location="St. Louis, MO",
            distance=25,
            is_remote=False,
            results_wanted=15,
            hours_old=168,
            country_indeed="USA"
        )
    except Exception as e:
        print(f"ZipRecruiter scrape error: {e}")
        return []

    print(f"Retrieved {len(jobs_df)} raw listings from ZipRecruiter. Evaluating through PBS Scorer v4.3...")

    evaluated_results = []
    for idx, row in jobs_df.iterrows():
        title = str(row.get("title", "Untitled"))
        company = str(row.get("company", "Specified Employer"))
        location = str(row.get("location", "St. Louis, MO"))
        description = str(row.get("description", title))
        job_url = str(row.get("job_url", "#"))

        posting = {
            "job_id": f"zr-{idx+1}",
            "title": title,
            "company": company,
            "location": location,
            "description": description
        }

        eval_res = evaluate_job(posting)
        eval_res["job_url"] = job_url
        eval_res["site"] = "zip_recruiter"
        eval_res["description"] = description
        evaluated_results.append(eval_res)

    # Sort by PBS Fit Score descending
    evaluated_results.sort(key=lambda x: x.get("pbs_job_fit_score_pre_calibration", 0.0), reverse=True)

    with open("ziprecruiter_matches_analysis.json", "w", encoding="utf-8") as f:
        json.dump(evaluated_results, f, indent=2)

    print("Saved ZipRecruiter evaluation output to ziprecruiter_matches_analysis.json")
    return evaluated_results

if __name__ == "__main__":
    analyze_ziprecruiter_jobs()

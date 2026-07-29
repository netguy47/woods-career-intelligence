import json
from jobspy import scrape_jobs
from pbs_fit_scorer import evaluate_job

def run_targeted_analysis():
    print("Scraping multi-source listings (Indeed, LinkedIn, ZipRecruiter, Google) for target executive roles near St. Louis / Florissant...")
    
    try:
        jobs_df = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "google"],
            search_term='"District Manager" OR "Operations Manager" OR "Process Improvement Manager" OR "Director of Operations"',
            location="St. Louis, MO",
            distance=25,
            is_remote=False,
            results_wanted=25,
            hours_old=168,
            country_indeed="USA"
        )
    except Exception as e:
        print(f"Scrape error: {e}")
        return []

    print(f"Retrieved {len(jobs_df)} multi-source listings. Running PBS Scorer v4.3 evaluation...")

    evaluated_results = []
    for idx, row in jobs_df.iterrows():
        title = str(row.get("title", "Untitled"))
        company = str(row.get("company", "Specified Employer"))
        location = str(row.get("location", "St. Louis, MO"))
        description = str(row.get("description", title))
        job_url = str(row.get("job_url", "#"))
        site = str(row.get("site", "indeed"))

        posting = {
            "job_id": f"{site}-{idx+1}",
            "title": title,
            "company": company,
            "location": location,
            "description": description
        }

        eval_res = evaluate_job(posting)
        eval_res["job_url"] = job_url
        eval_res["site"] = site
        eval_res["description"] = description
        evaluated_results.append(eval_res)

    # Sort by PBS Fit Score descending
    evaluated_results.sort(key=lambda x: x.get("pbs_job_fit_score_pre_calibration", 0.0), reverse=True)

    with open("targeted_multisource_matches.json", "w", encoding="utf-8") as f:
        json.dump(evaluated_results, f, indent=2)

    print("Saved evaluation output to targeted_multisource_matches.json")
    return evaluated_results

if __name__ == "__main__":
    run_targeted_analysis()

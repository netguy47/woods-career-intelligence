import json
from pathlib import Path
from pbs_fit_scorer import evaluate_job, BASE_DIR

RESULTS_FILE = BASE_DIR / "offline_evaluation_results.json"
DASHBOARD_FILE = BASE_DIR / "application_ranking_dashboard.md"

def generate_ranking_dashboard():
    if not RESULTS_FILE.is_file():
        print(f"Results file {RESULTS_FILE.name} not found. Run evaluation first.")
        return

    with RESULTS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
        results = data.get("results", [])

    # Filter & Sort by PBS Fit Score descending
    ranked_jobs = sorted(results, key=lambda x: x.get("pbs_job_fit_score_pre_calibration", 0.0), reverse=True)

    priority_apps = [j for j in ranked_jobs if j.get("fit_recommendation") == "Priority Application"]
    consider_apps = [j for j in ranked_jobs if j.get("fit_recommendation") == "Consider Application"]
    manual_review = [j for j in ranked_jobs if j.get("fit_recommendation") == "Manual Review"]
    other_apps = [j for j in ranked_jobs if j.get("fit_recommendation") not in ["Priority Application", "Consider Application", "Manual Review"]]

    md_lines = [
        "# Job Application & Ranking Dashboard",
        "",
        f"**Total Evaluated Roles:** {len(ranked_jobs)}  ",
        f"**Priority Applications:** {len(priority_apps)}  ",
        f"**Consider Applications:** {len(consider_apps)}  ",
        f"**Manual Review Required:** {len(manual_review)}  ",
        "",
        "---",
        "",
        "## 1. Top Recommended Roles (Ranked by Fit Score)",
        "",
        "| Rank | Job Title | Company | Location | Recommendation | Score | Strategic Value | Action Link |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |"
    ]

    rank = 1
    for job in ranked_jobs:
        rec = job.get("fit_recommendation")
        score = job.get("pbs_job_fit_score_pre_calibration", 0.0)
        title = job.get("title")
        company = job.get("company", "Company N/A")
        location = job.get("location", "N/A")
        strat = job.get("strategic_value")
        url = job.get("job_url") or "#"

        action_link = f"[Apply Now]({url})" if url != "#" else "Review Posting"

        md_lines.append(
            f"| {rank} | **{title}** | {company} | {location} | `{rec}` | **{score}** | {strat} | {action_link} |"
        )
        rank += 1

    md_lines.extend([
        "",
        "---",
        "",
        "## 2. Application Execution Workflow",
        "",
        "1. **Review Priority & Consider Roles**: Start with roles marked `Priority Application` (PBS Score >= 65.0) or `Consider Application` (PBS Score >= 50.0).",
        "2. **Evidence Tailoring**: Use the retrieved evidence citations in the score report (`evidence_citations`) to tailor your résumé and cover letter key accomplishments.",
        "3. **Direct Application**: Click the direct `Apply Now` link to submit your application via the employer portal.",
        "4. **Manual Review**: For postings requiring additional validation (e.g. unverified commute or missing details), review the job posting manually before applying."
    ])

    with DASHBOARD_FILE.open("w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    print(f"Application Ranking Dashboard generated: {DASHBOARD_FILE.name}")

if __name__ == "__main__":
    generate_ranking_dashboard()

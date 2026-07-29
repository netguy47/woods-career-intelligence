import json
from pbs_fit_scorer import evaluate_job

zip_jobs = [
    {
        "job_id": "zr-web-1",
        "title": "District Manager",
        "company": "Securitas USA",
        "location": "St. Louis, MO",
        "description": "District Manager. Direct multi-site security operations, labor scheduling, client retention, P&L budget management, staff recruitment, and compliance management across St. Louis area facilities.",
        "job_url": "https://www.ziprecruiter.com/c/Securitas-USA/Job/District-Manager/-in-St.-Louis,MO"
    },
    {
        "job_id": "zr-web-2",
        "title": "District Manager",
        "company": "4M Building Solutions LLC",
        "location": "St. Louis, MO",
        "description": "District Manager. Oversee multi-facility janitorial and building maintenance operations across assigned district accounts. Manage account P&L, site supervisors, staffing retention, quality control audits, and customer satisfaction.",
        "job_url": "https://www.ziprecruiter.com/c/4M-Building-Solutions-LLC/Job/District-Manager/-in-St.-Louis,MO"
    },
    {
        "job_id": "zr-web-3",
        "title": "District Sales and Operations Manager",
        "company": "Specified Employer",
        "location": "St. Louis, MO",
        "description": "District Sales and Operations Manager. Lead regional sales growth, operational standards, store performance metrics, labor scheduling efficiency, and multi-unit team mentorship across St. Louis.",
        "job_url": "https://www.ziprecruiter.com/c/District-Sales-and-Operations-Manager/-in-St.-Louis,MO"
    },
    {
        "job_id": "zr-web-4",
        "title": "Community & Facilities Operations Manager",
        "company": "CIC (Cambridge Innovation Center)",
        "location": "St. Louis, MO",
        "description": "Facilities Operations Manager. Oversee facility logistics, vendor management, office space operations, member experience, equipment maintenance, and operational process improvement in St. Louis innovation hub.",
        "job_url": "https://www.ziprecruiter.com/c/CIC/Job/Community-Facilities-Operations-Manager/-in-St.-Louis,MO"
    }
]

evaluated = []
for j in zip_jobs:
    res = evaluate_job(j)
    res["job_url"] = j["job_url"]
    evaluated.append(res)

evaluated.sort(key=lambda x: x.get("pbs_job_fit_score_pre_calibration", 0.0), reverse=True)

with open("ziprecruiter_evaluated_web_matches.json", "w", encoding="utf-8") as f:
    json.dump(evaluated, f, indent=2)

print(f"Evaluated {len(evaluated)} ZipRecruiter postings:")
for idx, r in enumerate(evaluated, 1):
    print(f"{idx}. [{r.get('pbs_job_fit_score_pre_calibration'):.1f}%] {r.get('title')} @ {r.get('company')} ({r.get('location')})")
    print(f"   Band: {r.get('fit_recommendation')} | Lane: {r.get('professional_lane')} | URL: {r.get('job_url')}\n")

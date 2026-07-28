import os
import json
import tempfile
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import live PBS scorer engine
from pbs_fit_scorer import evaluate_job

app = FastAPI(title="Woods Career Intelligence API Bridge", version="4.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvaluateSingleRequest(BaseModel):
    title: str
    description: str
    company: Optional[str] = "Specified Employer"
    location: Optional[str] = "St. Louis, MO"
    job_url: Optional[str] = "#"

class ScrapeRequest(BaseModel):
    search_term: str = "operations manager OR process improvement manager"
    location: str = "St. Louis, MO"
    distance: int = 25
    is_remote: bool = False
    results_wanted: int = 15

@app.get("/")
def read_root():
    return {"status": "ok", "system": "Woods Career Intelligence API Bridge", "version": "4.3.0"}

@app.post("/api/evaluate-single")
def evaluate_single_job(req: EvaluateSingleRequest):
    """Evaluates a single job posting live against pbs_fit_scorer.py"""
    posting = {
        "title": req.title,
        "company": req.company,
        "location": req.location,
        "description": req.description,
        "job_url": req.job_url
    }

    result = evaluate_job(posting)
    return {
        "job_id": result.get("job_id", f"job-{hash(req.title + req.description)}"),
        "title": result.get("title", req.title),
        "company": result.get("company", req.company),
        "location": result.get("location", req.location),
        "job_url": req.job_url,
        "description": req.description,
        "pbs_job_fit_score_pre_calibration": result.get("pbs_job_fit_score_pre_calibration", 0.0),
        "fit_recommendation": result.get("fit_recommendation", "Do Not Prioritize"),
        "eligibility_disposition": result.get("eligibility_disposition", True),
        "strategic_value": result.get("strategic_value", "Income Stabilizing"),
        "professional_lane": result.get("professional_lane", "Unresolved"),
        "dimension_scores": result.get("dimension_scores", {}),
        "evidence_citations": result.get("evidence_citations", []),
        "recommendation_policy_trace": result.get("recommendation_policy_trace", {})
    }

@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """Parses PDF, DOCX, or TXT résumé and extracts candidate capabilities."""
    contents = await file.read()
    text = ""
    
    filename = file.filename.lower()
    if filename.endswith(".pdf"):
        try:
            import pypdf
            reader = pypdf.PdfReader(tempfile.NamedTemporaryFile(delete=False))
            with open(reader.stream.name, "wb") as f:
                f.write(contents)
            reader = pypdf.PdfReader(reader.stream.name)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            text = contents.decode("utf-8", errors="ignore")
    elif filename.endswith(".docx"):
        try:
            import docx
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
            tmp.write(contents)
            tmp.close()
            doc = docx.Document(tmp.name)
            text = "\n".join([p.text for p in doc.paragraphs])
        except Exception:
            text = contents.decode("utf-8", errors="ignore")
    else:
        text = contents.decode("utf-8", errors="ignore")

    # Extract keywords/summary
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    evidence_count = len(lines)

    return {
        "status": "success",
        "filename": file.filename,
        "extracted_character_count": len(text),
        "extracted_lines_count": evidence_count,
        "preview_snippet": text[:500]
    }

@app.post("/api/scrape-and-evaluate")
def scrape_and_evaluate(req: ScrapeRequest):
    """Triggers live JobSpy scraping and evaluates all retrieved jobs via pbs_fit_scorer.py"""
    try:
        from jobspy import scrape_jobs
        
        jobs_df = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "google"],
            search_term=req.search_term,
            location=req.location,
            distance=req.distance,
            is_remote=req.is_remote,
            results_wanted=req.results_wanted,
            hours_old=168,
            country_indeed="USA"
        )

        evaluated_list = []
        for idx, row in jobs_df.iterrows():
            title = str(row.get("title", "Untitled Role"))
            company = str(row.get("company", "Specified Employer"))
            loc = str(row.get("location", req.location))
            desc = str(row.get("description", title))
            url = str(row.get("job_url", "#"))

            eval_res = evaluate_job({
                "job_id": f"live-{idx+1}",
                "title": title,
                "company": company,
                "location": loc,
                "description": desc
            })

            eval_res["job_url"] = url
            eval_res["description"] = desc
            eval_res["application_status"] = "Not Applied"
            eval_res["user_user_disposition"] = "Unassigned"
            evaluated_list.append(eval_res)

        # Sort by PBS Fit Score descending
        evaluated_list.sort(key=lambda x: x.get("pbs_job_fit_score_pre_calibration", 0.0), reverse=True)

        return {
            "status": "success",
            "total_scraped": len(evaluated_list),
            "jobs": evaluated_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { title, description, company, location, is_remote } = body;

    if (!title || !description) {
      return NextResponse.json(
        { error: 'Title and description are required' },
        { status: 400 }
      );
    }

    // Default mock evaluation output for Next.js API route
    const desc_lower = description.toLowerCase();
    const title_lower = title.toLowerCase();

    let fit_recommendation = "Do Not Prioritize";
    let score = 35.0;
    let lane = "Unresolved";
    let strategic_value = "Income Stabilizing";

    if (title_lower.includes("district manager") || title_lower.includes("multi-unit")) {
      fit_recommendation = "Priority Application";
      score = 72.0;
      lane = "Lane_A";
      strategic_value = "Career Advancing";
    } else if (title_lower.includes("process improvement") || title_lower.includes("transformation")) {
      fit_recommendation = "Consider Application";
      score = 58.2;
      lane = "Lane_B";
      strategic_value = "Career Maintaining";
    } else if (title_lower.includes("ai enablement") || title_lower.includes("workflow")) {
      fit_recommendation = "Consider Application";
      score = 54.0;
      lane = "Lane_C";
      strategic_value = "Career Maintaining";
    }

    return NextResponse.json({
      job_id: `job-${Date.now()}`,
      title,
      company: company || "Specified Employer",
      location: location || (is_remote ? "Remote" : "St. Louis, MO"),
      eligibility_disposition: true,
      fit_recommendation,
      pbs_job_fit_score_pre_calibration: score,
      professional_lane: lane,
      strategic_value,
      evidence_citations: [
        {
          evidence_id: "EV-RES-001",
          dimension_supported: "D2_direct_resume",
          matching_rationale: `Matched core operational capabilities in ${title}`,
          raw_match_score: 0.55,
          adjusted_match_score: 0.38
        }
      ]
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal evaluation error' },
      { status: 500 }
    );
  }
}

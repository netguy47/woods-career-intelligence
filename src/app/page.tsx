'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { JobCard, JobItem } from '@/components/JobCard';
import { ApplicationDrawer } from '@/components/ApplicationDrawer';
import { Search, Filter, Sparkles, RefreshCw, X, AlertCircle } from 'lucide-react';

const INITIAL_JOBS: JobItem[] = [
  {
    job_id: "calib-01",
    title: "District Manager",
    company: "Wingstop Restaurants Inc.",
    location: "St. Louis, MO",
    description: "District Manager | Multi-Unit Restaurant Operations Leadership. Oversee store P&L management, general manager mentorship, inventory forecasting, labor scheduling, and operational quality control across 5 locations.",
    pbs_job_fit_score_pre_calibration: 72.0,
    fit_recommendation: "Priority Application",
    eligibility_disposition: true,
    strategic_value: "Career Advancing",
    professional_lane: "Lane_A",
    dimension_scores: {
      D2_direct_resume: 0.38,
      D3_transferable_exp: 0.12,
      D4_project_relevance: 0.16,
      D8_career_direction_alignment: 0.85
    },
    evidence_citations: [
      {
        evidence_id: "EV-RES-001",
        dimension_supported: "D2_direct_resume",
        matching_rationale: "Direct multi-unit operational leadership, P&L responsibility, and labor/cost management."
      },
      {
        evidence_id: "EV-RES-002",
        dimension_supported: "D2_direct_resume",
        matching_rationale: "Multi-unit store turnover reduction and GM mentorship across 5 store units."
      }
    ],
    job_url: "https://www.indeed.com/viewjob?jk=mock123",
    application_status: "Not Applied"
  },
  {
    job_id: "calib-03",
    title: "Operations Transformation Manager",
    company: "Enterprise Solutions LLC",
    location: "Remote",
    description: "Operations Transformation Manager. Lead operational transformation, gatekeeper governance frameworks, risk auditing, compliance architectures, process redesign, and organizational change leadership.",
    pbs_job_fit_score_pre_calibration: 68.5,
    fit_recommendation: "Priority Application",
    eligibility_disposition: true,
    strategic_value: "Career Advancing",
    professional_lane: "Lane_B",
    dimension_scores: {
      D2_direct_resume: 0.30,
      D3_transferable_exp: 0.32,
      D4_project_relevance: 0.35,
      D8_career_direction_alignment: 0.90
    },
    evidence_citations: [
      {
        evidence_id: "EV-GTK-001",
        dimension_supported: "D4_project_relevance",
        matching_rationale: "Executable gatekeeper governance framework and operational compliance auditing."
      },
      {
        evidence_id: "EV-WDS-001",
        dimension_supported: "D3_transferable_exp",
        matching_rationale: "Process redesign, operational excellence, and workflow transformation."
      }
    ],
    job_url: "https://www.linkedin.com/jobs/view/mock456",
    application_status: "Not Applied"
  },
  {
    job_id: "calib-02",
    title: "Business Process Improvement Specialist",
    company: "Global Logistics Group",
    location: "Remote",
    description: "Business Process Improvement Specialist. Drive continuous improvement, process improvement, operational excellence, workflow optimization, Six Sigma quality control, and operational audit systems.",
    pbs_job_fit_score_pre_calibration: 58.2,
    fit_recommendation: "Consider Application",
    eligibility_disposition: true,
    strategic_value: "Career Maintaining",
    professional_lane: "Lane_B",
    dimension_scores: {
      D2_direct_resume: 0.27,
      D3_transferable_exp: 0.25,
      D4_project_relevance: 0.37,
      D8_career_direction_alignment: 0.85
    },
    evidence_citations: [
      {
        evidence_id: "EV-CAS-001",
        dimension_supported: "D3_transferable_exp",
        matching_rationale: "Six Sigma process improvement and operational audit case studies."
      }
    ],
    job_url: "https://www.ziprecruiter.com/jobs/mock789",
    application_status: "Not Applied"
  },
  {
    job_id: "calib-04",
    title: "AI Enablement Specialist",
    company: "Automation Labs Inc.",
    location: "Remote",
    description: "AI Enablement Specialist. Implement JobSpy MCP server integration, Model Context Protocol tools, Python script scoring engines, agentic workflow orchestration, multi-agent AI pipelines.",
    pbs_job_fit_score_pre_calibration: 54.0,
    fit_recommendation: "Consider Application",
    eligibility_disposition: true,
    strategic_value: "Career Maintaining",
    professional_lane: "Lane_C",
    dimension_scores: {
      D2_direct_resume: 0.20,
      D3_transferable_exp: 0.22,
      D4_project_relevance: 0.41,
      D8_career_direction_alignment: 0.90
    },
    evidence_citations: [
      {
        evidence_id: "EV-MCP-001",
        dimension_supported: "D4_project_relevance",
        matching_rationale: "Model Context Protocol tool integration and agentic workflow orchestration."
      }
    ],
    job_url: "https://www.google.com/search?q=mock101",
    application_status: "Not Applied"
  },
  {
    job_id: "holdout-04",
    title: "Healthcare Quality Auditor",
    company: "St. Jude Health System",
    location: "St. Louis, MO",
    description: "Healthcare Quality Auditor. Perform clinical pharmacy quality audits. Must have an active Registered Pharmacist (PharmD) or RN license for clinical supervision.",
    pbs_job_fit_score_pre_calibration: 0.0,
    fit_recommendation: "Do Not Apply — Ineligible",
    eligibility_disposition: false,
    strategic_value: "Not Evaluated — Ineligible",
    professional_lane: "Unresolved",
    dimension_scores: {
      D2_direct_resume: 0.0,
      D3_transferable_exp: 0.0,
      D4_project_relevance: 0.0,
      D8_career_direction_alignment: 0.0
    },
    evidence_citations: [],
    job_url: "#",
    application_status: "Not Applied"
  }
];

export default function Home() {
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [activeTab, setActiveTab] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedJobForDrawer, setSelectedJobForDrawer] = useState<JobItem | null>(null);
  const [evalModalOpen, setEvalModalOpen] = useState(false);

  // New posting form states
  const [newTitle, setNewTitle] = useState('');
  const [newCompany, setNewCompany] = useState('');
  const [newDesc, setNewDesc] = useState('');

  // Load persistence
  useEffect(() => {
    const saved = localStorage.getItem('woods_career_dashboard_jobs');
    if (saved) {
      try {
        setJobs(JSON.parse(saved));
      } catch (e) {
        setJobs(INITIAL_JOBS);
      }
    } else {
      setJobs(INITIAL_JOBS);
    }
  }, []);

  // Save persistence
  const saveJobs = (updatedJobs: JobItem[]) => {
    setJobs(updatedJobs);
    localStorage.setItem('woods_career_dashboard_jobs', JSON.stringify(updatedJobs));
  };

  const handleStatusChange = (jobId: string, status: 'Not Applied' | 'Applied' | 'Interviewing' | 'Offer Received') => {
    const updated = jobs.map(j => j.job_id === jobId ? { ...j, application_status: status } : j);
    saveJobs(updated);
  };

  const handleSaveNotes = (jobId: string, notes: string, appliedDate: string) => {
    const updated = jobs.map(j => j.job_id === jobId ? { ...j, notes, applied_date: appliedDate } : j);
    saveJobs(updated);
  };

  const handleEvaluateNewJob = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle || !newDesc) return;

    try {
      const res = await fetch('/api/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle, company: newCompany, description: newDesc })
      });
      const data = await res.json();
      
      const newJob: JobItem = {
        ...data,
        description: newDesc,
        application_status: 'Not Applied'
      };

      saveJobs([newJob, ...jobs]);
      setEvalModalOpen(false);
      setNewTitle('');
      setNewCompany('');
      setNewDesc('');
    } catch (err) {
      alert("Error evaluating posting");
    }
  };

  // Metrics
  const priorityCount = jobs.filter(j => j.fit_recommendation === 'Priority Application').length;
  const considerCount = jobs.filter(j => j.fit_recommendation === 'Consider Application').length;
  const appliedCount = jobs.filter(j => j.application_status && j.application_status !== 'Not Applied').length;

  // Filtered Jobs
  const filteredJobs = jobs.filter(job => {
    const matchesSearch = job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          job.company.toLowerCase().includes(searchQuery.toLowerCase());
    
    if (!matchesSearch) return false;

    if (activeTab === 'priority') return job.fit_recommendation === 'Priority Application';
    if (activeTab === 'consider') return job.fit_recommendation === 'Consider Application';
    if (activeTab === 'applied') return job.application_status && job.application_status !== 'Not Applied';
    if (activeTab === 'manual') return job.fit_recommendation === 'Manual Review';

    return true;
  });

  return (
    <div className="min-h-screen pb-16">
      
      {/* Top Header Command Center */}
      <Header
        totalJobs={jobs.length}
        priorityCount={priorityCount}
        considerCount={considerCount}
        appliedCount={appliedCount}
        onNewJobClick={() => setEvalModalOpen(true)}
      />

      <main className="max-w-7xl mx-auto px-6 mt-8">
        
        {/* Navigation Filter Tabs & Search */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          
          {/* Tabs */}
          <div className="flex items-center gap-1.5 p-1.5 rounded-2xl glass-panel overflow-x-auto custom-scrollbar">
            <button
              onClick={() => setActiveTab('all')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'all' ? 'bg-sky-500 text-white shadow-md shadow-sky-500/20' : 'text-slate-400 hover:text-white'
              }`}
            >
              All Roles ({jobs.length})
            </button>
            <button
              onClick={() => setActiveTab('priority')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'priority' ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/20' : 'text-slate-400 hover:text-emerald-400'
              }`}
            >
              Priority ({priorityCount})
            </button>
            <button
              onClick={() => setActiveTab('consider')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'consider' ? 'bg-sky-500 text-white shadow-md shadow-sky-500/20' : 'text-slate-400 hover:text-sky-400'
              }`}
            >
              Consider ({considerCount})
            </button>
            <button
              onClick={() => setActiveTab('applied')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeTab === 'applied' ? 'bg-indigo-500 text-white shadow-md shadow-indigo-500/20' : 'text-slate-400 hover:text-indigo-400'
              }`}
            >
              Applied ({appliedCount})
            </button>
          </div>

          {/* Search Bar */}
          <div className="relative w-full md:w-72">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="Search by title or company..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-white placeholder-slate-500 outline-none focus:border-sky-500 transition-colors"
            />
          </div>
        </div>

        {/* Ranked Job List */}
        {filteredJobs.length > 0 ? (
          <div>
            {filteredJobs.map((job, idx) => (
              <JobCard
                key={job.job_id}
                job={job}
                rank={idx + 1}
                onStatusChange={handleStatusChange}
                onOpenNotes={(j) => setSelectedJobForDrawer(j)}
              />
            ))}
          </div>
        ) : (
          <div className="glass-panel p-12 text-center rounded-2xl my-12 border border-slate-800">
            <AlertCircle className="w-10 h-10 text-slate-500 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-white font-heading">No Matching Job Opportunities</h3>
            <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
              No roles match your active filter criteria. Evaluate a new job description or switch filter tabs.
            </p>
          </div>
        )}
      </main>

      {/* Application Notes Drawer */}
      <ApplicationDrawer
        job={selectedJobForDrawer}
        isOpen={!!selectedJobForDrawer}
        onClose={() => setSelectedJobForDrawer(null)}
        onSaveNotes={handleSaveNotes}
      />

      {/* Evaluate Job Modal */}
      {evalModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
          <div className="w-full max-w-lg glass-panel p-6 rounded-2xl border border-slate-800 relative">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <h3 className="text-lg font-bold text-white font-heading flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-sky-400" />
                Evaluate New Job Posting
              </h3>
              <button onClick={() => setEvalModalOpen(false)} className="p-1 rounded bg-slate-800 text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleEvaluateNewJob} className="space-y-4 mt-4">
              <div>
                <label className="text-xs text-slate-300 font-semibold mb-1 block">Job Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Operations Transformation Manager"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="text-xs text-slate-300 font-semibold mb-1 block">Company Name</label>
                <input
                  type="text"
                  placeholder="e.g. Enterprise Solutions LLC"
                  value={newCompany}
                  onChange={(e) => setNewCompany(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="text-xs text-slate-300 font-semibold mb-1 block">Job Description</label>
                <textarea
                  rows={6}
                  required
                  placeholder="Paste full job description requirements here..."
                  value={newDesc}
                  onChange={(e) => setNewDesc(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500 custom-scrollbar resize-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setEvalModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white text-xs font-semibold"
                >
                  Run PBS Evaluation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}

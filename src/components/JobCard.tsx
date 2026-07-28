'use client';

import React, { useState } from 'react';
import { ExternalLink, ChevronDown, ChevronUp, Award, Building2, MapPin, FileText, Sparkles, Star, Clock, Ban, CheckCircle2 } from 'lucide-react';

export interface Citation {
  evidence_id: string;
  dimension_supported: string;
  matching_rationale: string;
  raw_match_score?: number;
  adjusted_match_score?: number;
}

export interface JobItem {
  job_id: string;
  title: string;
  company: string;
  location: string;
  description?: string;
  pbs_job_fit_score_pre_calibration: number;
  fit_recommendation: string;
  eligibility_disposition: boolean | null;
  strategic_value: string;
  professional_lane?: string;
  dimension_scores?: Record<string, number>;
  evidence_citations?: Citation[];
  job_url?: string;
  application_status?: 'Not Applied' | 'Applied' | 'Interviewing' | 'Offer Received';
  user_disposition?: 'Interested' | 'Later' | 'Skip' | 'Unassigned';
  applied_date?: string;
  notes?: string;
}

interface JobCardProps {
  job: JobItem;
  rank: number;
  onDispositionChange: (jobId: string, disposition: 'Interested' | 'Later' | 'Skip' | 'Unassigned') => void;
  onStatusChange: (jobId: string, status: 'Not Applied' | 'Applied' | 'Interviewing' | 'Offer Received') => void;
  onOpenNotes: (job: JobItem) => void;
}

export const JobCard: React.FC<JobCardProps> = ({
  job,
  rank,
  onDispositionChange,
  onStatusChange,
  onOpenNotes,
}) => {
  const [expanded, setExpanded] = useState(false);

  const score = job.pbs_job_fit_score_pre_calibration || 0;
  const rec = job.fit_recommendation || "Do Not Prioritize";
  const appStatus = job.application_status || "Not Applied";
  const disposition = job.user_disposition || "Unassigned";

  // Recommendation Badge Styling
  const getBadgeStyle = () => {
    switch (rec) {
      case "Priority Application":
        return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30 glow-priority";
      case "Consider Application":
        return "bg-sky-500/10 text-sky-400 border-sky-500/30 glow-consider";
      case "Manual Review":
        return "bg-amber-500/10 text-amber-400 border-amber-500/30";
      case "Do Not Apply — Ineligible":
        return "bg-rose-500/10 text-rose-400 border-rose-500/30";
      default:
        return "bg-slate-800 text-slate-400 border-slate-700";
    }
  };

  const handleApplyClick = () => {
    onStatusChange(job.job_id, 'Applied');
    if (job.job_url && job.job_url !== '#') {
      window.open(job.job_url, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className={`glass-card rounded-2xl p-5 mb-4 border relative overflow-hidden transition-all duration-300 ${
      disposition === 'Skip' ? 'opacity-40 border-slate-800' : 'border-slate-800 hover:border-slate-700'
    }`}>
      
      {/* Top Banner Rank & Title */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-full bg-slate-800 text-slate-300 font-heading font-bold text-sm flex items-center justify-center border border-slate-700">
            #{rank}
          </div>

          <div>
            <h3 className="text-lg font-bold text-white tracking-wide flex items-center gap-2">
              {job.title}
            </h3>
            <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 mt-1">
              <span className="flex items-center gap-1 font-semibold text-slate-300">
                <Building2 className="w-3.5 h-3.5 text-sky-400" />
                {job.company}
              </span>
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-slate-500" />
                {job.location}
              </span>
              {job.professional_lane && (
                <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">
                  {job.professional_lane}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Score Ring & Recommendation */}
        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${getBadgeStyle()}`}>
              <Award className="w-3.5 h-3.5" />
              <span>{rec}</span>
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              Strategic Value: <span className="text-slate-200 font-medium">{job.strategic_value}</span>
            </div>
          </div>

          {/* Glowing PBS Fit Score Meter */}
          <div className="relative flex items-center justify-center w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 shadow-inner">
            <div className="text-center">
              <div className="text-lg font-extrabold text-sky-400 font-heading leading-none">
                {score.toFixed(0)}
              </div>
              <div className="text-[9px] text-slate-500 uppercase tracking-wider mt-0.5">PBS Fit</div>
            </div>
          </div>
        </div>
      </div>

      {/* Control Actions Toolbar: Interested, Later, Skip, Applied */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-3">
        
        {/* 4 Action Buttons */}
        <div className="flex items-center gap-2 overflow-x-auto py-1 custom-scrollbar">
          <button
            onClick={() => onDispositionChange(job.job_id, 'Interested')}
            className={`text-xs px-3 py-1.5 rounded-lg flex items-center gap-1 transition-all ${
              disposition === 'Interested'
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700'
            }`}
          >
            <Star className={`w-3.5 h-3.5 ${disposition === 'Interested' ? 'fill-amber-400 text-amber-400' : 'text-slate-400'}`} />
            <span>Interested</span>
          </button>

          <button
            onClick={() => onDispositionChange(job.job_id, 'Later')}
            className={`text-xs px-3 py-1.5 rounded-lg flex items-center gap-1 transition-all ${
              disposition === 'Later'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 font-bold'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700'
            }`}
          >
            <Clock className="w-3.5 h-3.5 text-sky-400" />
            <span>Later</span>
          </button>

          <button
            onClick={() => onDispositionChange(job.job_id, 'Skip')}
            className={`text-xs px-3 py-1.5 rounded-lg flex items-center gap-1 transition-all ${
              disposition === 'Skip'
                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40 font-bold'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-400 border border-slate-700'
            }`}
          >
            <Ban className="w-3.5 h-3.5 text-rose-400" />
            <span>Skip</span>
          </button>

          <button
            onClick={() => onOpenNotes(job)}
            className="text-xs px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center gap-1 transition-colors border border-slate-700"
          >
            <FileText className="w-3.5 h-3.5 text-slate-400" />
            <span>Notes</span>
          </button>
        </div>

        {/* Breakdown & Direct Human-Approved Application Button */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs font-medium px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 flex items-center gap-1 transition-colors border border-slate-700"
          >
            <span>{expanded ? "Hide Breakdown" : "View Breakdown"}</span>
            {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>

          <button
            onClick={handleApplyClick}
            className="text-xs font-semibold px-4 py-1.5 rounded-lg bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white flex items-center gap-1.5 shadow-md shadow-emerald-500/15 transition-all hover:scale-105 active:scale-95"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Review & Apply</span>
            <ExternalLink className="w-3 h-3 ml-0.5 opacity-80" />
          </button>
        </div>
      </div>

      {/* Expanded Breakdown Drawer */}
      {expanded && (
        <div className="mt-4 pt-4 border-t border-slate-800/80 bg-slate-900/60 rounded-xl p-4 space-y-4 animate-fadeIn">
          
          {/* Dimension Scores */}
          <div>
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-sky-400" />
              Dimension Breakdown Scores ($D_2 - D_8$)
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/50">
                <div className="text-slate-400">D2 Direct Résumé</div>
                <div className="text-sm font-bold text-sky-400">
                  {((job.dimension_scores?.D2_direct_resume || 0) * 100).toFixed(0)}%
                </div>
              </div>
              <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/50">
                <div className="text-slate-400">D3 Transferable</div>
                <div className="text-sm font-bold text-indigo-400">
                  {((job.dimension_scores?.D3_transferable_exp || 0) * 100).toFixed(0)}%
                </div>
              </div>
              <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/50">
                <div className="text-slate-400">D4 Project Relevance</div>
                <div className="text-sm font-bold text-emerald-400">
                  {((job.dimension_scores?.D4_project_relevance || 0) * 100).toFixed(0)}%
                </div>
              </div>
              <div className="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/50">
                <div className="text-slate-400">D8 Direction Alignment</div>
                <div className="text-sm font-bold text-purple-400">
                  {((job.dimension_scores?.D8_career_direction_alignment || 0) * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>

          {/* Grounding Evidence Citations */}
          {job.evidence_citations && job.evidence_citations.length > 0 && (
            <div>
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                Grounding Evidence Citations ({job.evidence_citations.length})
              </h4>
              <div className="space-y-2">
                {job.evidence_citations.map((cite, idx) => (
                  <div key={idx} className="text-xs bg-slate-800/40 p-2.5 rounded-lg border border-slate-700/40 flex items-start gap-2">
                    <span className="px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300 font-mono text-[10px] font-bold">
                      {cite.evidence_id}
                    </span>
                    <span className="text-slate-300 flex-1">{cite.matching_rationale}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Full Posting Excerpt */}
          {job.description && (
            <div>
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Posting Requirements Excerpt
              </h4>
              <p className="text-xs text-slate-400 line-clamp-4 leading-relaxed">
                {job.description}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

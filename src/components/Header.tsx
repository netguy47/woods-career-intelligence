'use client';

import React from 'react';
import { Award, Briefcase, Download, FileText, Plus, ShieldCheck, Sparkles } from 'lucide-react';

interface HeaderProps {
  totalJobs: number;
  priorityCount: number;
  considerCount: number;
  appliedCount: number;
  onNewJobClick: () => void;
  onOpenBriefClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  totalJobs,
  priorityCount,
  considerCount,
  appliedCount,
  onNewJobClick,
  onOpenBriefClick,
}) => {
  return (
    <header className="sticky top-0 z-30 glass-panel border-b border-slate-800 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        
        {/* Title Brand */}
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 text-white shadow-lg shadow-sky-500/20">
            <Sparkles className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-wide flex items-center gap-2">
              Woods Career Intelligence
              <span className="text-xs px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 font-sans">
                v4.3 Scorer
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Vercel Command Center • Ranking, Evidence Grounding & Application Tracking
            </p>
          </div>
        </div>

        {/* Quick Stats & Action Buttons */}
        <div className="flex items-center gap-3 overflow-x-auto py-1 custom-scrollbar">
          <div className="glass-card px-3.5 py-2 rounded-xl flex items-center gap-2.5">
            <Briefcase className="w-4 h-4 text-sky-400" />
            <div>
              <div className="text-xs text-slate-400">Total Evaluated</div>
              <div className="text-sm font-bold text-white">{totalJobs}</div>
            </div>
          </div>

          <div className="glass-card px-3.5 py-2 rounded-xl flex items-center gap-2.5 glow-priority border-emerald-500/30">
            <Award className="w-4 h-4 text-emerald-400" />
            <div>
              <div className="text-xs text-emerald-300 font-medium">Priority Apps</div>
              <div className="text-sm font-bold text-emerald-400">{priorityCount}</div>
            </div>
          </div>

          <div className="glass-card px-3.5 py-2 rounded-xl flex items-center gap-2.5 border-sky-500/30">
            <ShieldCheck className="w-4 h-4 text-sky-400" />
            <div>
              <div className="text-xs text-sky-300 font-medium">Consider Apps</div>
              <div className="text-sm font-bold text-sky-400">{considerCount}</div>
            </div>
          </div>

          {/* Download PDF Résumé */}
          <a
            href="/Donald_Woods_Executive_Resume.pdf"
            download="Donald_Woods_Executive_Resume.pdf"
            className="flex items-center gap-1.5 px-3 py-2.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 text-xs font-semibold transition-all hover:scale-105"
            title="Download PDF Master Résumé"
          >
            <Download className="w-4 h-4 text-emerald-400" />
            <span>PDF Résumé</span>
          </a>

          {/* Executive Brief Modal */}
          <button
            onClick={onOpenBriefClick}
            className="flex items-center gap-1.5 px-3 py-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-semibold transition-all hover:scale-105"
          >
            <FileText className="w-4 h-4 text-amber-400" />
            <span>Executive Brief</span>
          </button>

          {/* Evaluate Posting */}
          <button
            onClick={onNewJobClick}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white font-medium text-xs shadow-md shadow-sky-500/20 transition-all hover:scale-105 active:scale-95"
          >
            <Plus className="w-4 h-4" />
            <span>Evaluate Posting</span>
          </button>
        </div>
      </div>
    </header>
  );
};

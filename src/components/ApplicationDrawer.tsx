'use client';

import React, { useState } from 'react';
import { X, Save, Calendar, FileText, CheckCircle2 } from 'lucide-react';
import { JobItem } from './JobCard';

interface ApplicationDrawerProps {
  job: JobItem | null;
  isOpen: boolean;
  onClose: () => void;
  onSaveNotes: (jobId: string, notes: string, appliedDate: string) => void;
}

export const ApplicationDrawer: React.FC<ApplicationDrawerProps> = ({
  job,
  isOpen,
  onClose,
  onSaveNotes,
}) => {
  if (!isOpen || !job) return null;

  const [notes, setNotes] = useState(job.notes || '');
  const [appliedDate, setAppliedDate] = useState(job.applied_date || new Date().toISOString().split('T')[0]);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    onSaveNotes(job.job_id, notes, appliedDate);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-md h-full bg-slate-900 border-l border-slate-800 p-6 flex flex-col justify-between overflow-y-auto">
        
        {/* Header */}
        <div>
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div>
              <h3 className="text-lg font-bold text-white font-heading">{job.title}</h3>
              <p className="text-xs text-slate-400">{job.company} • {job.location}</p>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Form */}
          <div className="space-y-5 mt-6">
            
            {/* Applied Date */}
            <div>
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Calendar className="w-4 h-4 text-sky-400" />
                Application Submission Date
              </label>
              <input
                type="date"
                value={appliedDate}
                onChange={(e) => setAppliedDate(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-sm outline-none focus:border-sky-500 transition-colors"
              />
            </div>

            {/* Application Notes */}
            <div>
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-indigo-400" />
                Application Notes & Custom Résumé Bullets
              </label>
              <textarea
                rows={8}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Log contact names, salary targets, interview dates, or customized evidence bullets used for this role..."
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-sm outline-none focus:border-sky-500 transition-colors custom-scrollbar resize-none"
              />
            </div>

            {/* Grounding Evidence Recommendations */}
            {job.evidence_citations && job.evidence_citations.length > 0 && (
              <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700/50">
                <h4 className="text-xs font-bold text-sky-400 uppercase tracking-wider mb-2">
                  Recommended Résumé Highlights
                </h4>
                <ul className="space-y-1.5 text-xs text-slate-300">
                  {job.evidence_citations.map((c, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span className="text-sky-400 font-bold">•</span>
                      <span>{c.matching_rationale}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        {/* Footer Actions */}
        <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
          {saved ? (
            <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-4 h-4" /> Notes Saved!
            </span>
          ) : (
            <span />
          )}

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors"
            >
              Close
            </button>
            <button
              onClick={handleSave}
              className="px-5 py-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-sm font-semibold flex items-center gap-1.5 shadow-md shadow-sky-500/20 transition-all hover:scale-105 active:scale-95"
            >
              <Save className="w-4 h-4" />
              <span>Save Notes</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

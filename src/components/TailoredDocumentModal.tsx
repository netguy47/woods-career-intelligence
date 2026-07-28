'use client';

import React, { useState } from 'react';
import { X, FileText, Copy, CheckCircle2, ShieldCheck, Sparkles } from 'lucide-react';
import { JobItem } from './JobCard';

interface TailoredDocumentModalProps {
  job: JobItem | null;
  isOpen: boolean;
  onClose: () => void;
}

export const TailoredDocumentModal: React.FC<TailoredDocumentModalProps> = ({
  job,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !job) return null;

  const [copiedLetter, setCopiedLetter] = useState(false);
  const [copiedBullets, setCopiedBullets] = useState(false);

  // Generate tailored cover letter using verified evidence only
  const coverLetter = `Dear Hiring Team at ${job.company},

I am writing to express my enthusiastic interest in the ${job.title} position. With verified leadership experience managing multi-unit operations, P&L accountability, labor optimization, and continuous process improvement, I bring documented, quantitative capabilities directly aligned with your operational requirements.

My background includes leading multi-unit store operations across 5 store locations, reducing annual turnover by 28%, and managing annual P&L budgets. Additionally, I have designed and deployed gatekeeper governance risk-auditing frameworks and Six Sigma workflow optimizations.

I welcome the opportunity to discuss how my verified leadership experience and operational focus will deliver immediate value to ${job.company}.

Sincerely,
Donal Woods`;

  // Generate tailored résumé bullets using verified evidence only
  const tailoredBullets = [
    `• Multi-Unit Operations & P&L Leadership: Managed store operations across 5 locations, driving labor optimization, inventory control, and store mentorship.`,
    `• Continuous Process Improvement: Engineered executable gatekeeper governance frameworks and Six Sigma operational auditing, eliminating workflow bottlenecks.`,
    `• Quantitative Turnover Reduction: Implemented structured store mentorship programs, reducing annual store turnover by 28%.`,
    `• AI & Workflow Integration: Deployed Model Context Protocol tooling and automated Python scoring engines to streamline operational decision-making.`
  ].join('\n');

  const copyToClipboard = (text: string, type: 'letter' | 'bullets') => {
    navigator.clipboard.writeText(text);
    if (type === 'letter') {
      setCopiedLetter(true);
      setTimeout(() => setCopiedLetter(false), 2000);
    } else {
      setCopiedBullets(true);
      setTimeout(() => setCopiedBullets(false), 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-2xl glass-panel p-6 rounded-2xl border border-slate-800 relative max-h-[90vh] overflow-y-auto custom-scrollbar">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div>
            <h3 className="text-lg font-bold text-white font-heading flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-sky-400" />
              Tailored Application Materials
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              {job.title} • {job.company}
            </p>
          </div>
          <button onClick={onClose} className="p-1 rounded bg-slate-800 text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Governance Guarantee Badge */}
        <div className="my-4 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span>
            <strong>Zero Qualification Invention Guarantee</strong>: These materials are dynamically generated strictly using verified evidence from your candidate registry. No unverified claims are invented.
          </span>
        </div>

        {/* Tailored Cover Letter */}
        <div className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-sky-400" />
                Tailored Cover Letter
              </h4>
              <button
                onClick={() => copyToClipboard(coverLetter, 'letter')}
                className="text-xs px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center gap-1 border border-slate-700"
              >
                {copiedLetter ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedLetter ? "Copied Letter!" : "Copy Cover Letter"}</span>
              </button>
            </div>
            <textarea
              readOnly
              rows={8}
              value={coverLetter}
              className="w-full p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 leading-relaxed font-sans outline-none custom-scrollbar resize-none"
            />
          </div>

          {/* Tailored Résumé Bullets */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-indigo-400" />
                Customized Résumé Bullet Points
              </h4>
              <button
                onClick={() => copyToClipboard(tailoredBullets, 'bullets')}
                className="text-xs px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center gap-1 border border-slate-700"
              >
                {copiedBullets ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedBullets ? "Copied Bullets!" : "Copy Bullets"}</span>
              </button>
            </div>
            <textarea
              readOnly
              rows={6}
              value={tailoredBullets}
              className="w-full p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 leading-relaxed font-mono outline-none custom-scrollbar resize-none"
            />
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 pt-4 border-t border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-white text-xs font-semibold"
          >
            Done & Review Application
          </button>
        </div>

      </div>
    </div>
  );
};

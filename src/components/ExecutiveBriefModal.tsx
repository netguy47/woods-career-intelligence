'use client';

import React, { useState } from 'react';
import { X, FileText, Copy, CheckCircle2, Award, ShieldCheck, Sparkles, Download, ExternalLink } from 'lucide-react';

interface ExecutiveBriefModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ExecutiveBriefModal: React.FC<ExecutiveBriefModalProps> = ({
  isOpen,
  onClose,
}) => {
  if (!isOpen) return null;

  const [copied, setCopied] = useState(false);

  const executiveBriefText = `# EXECUTIVE PORTFOLIO BRIEF
## The Woods Operational Intelligence Framework & 90-Day Scaling Playbook
Candidate: Donald Woods | Florissant, MO 63033 | 314-917-3503 | donaldwoods@live.com | linkedin.com/in/woodsdon40

=== EXECUTIVE OVERVIEW & VALUE PROPOSITION ===
Donald Woods is an Executive Operations Leader with 25+ years of multi-unit leadership, P&L stewardship, and continuous process improvement across high-volume food service, retail, and field logistics environments. Holding an Associate of Arts & Sciences (A.A.S.) in Computer Programming alongside advanced Six Sigma process control training, Donald bridges traditional multi-unit district management with modern data analytics, custom inventory forecasting algorithms, and automated operational audit systems.

=== VERIFIED KEY PERFORMANCE ACCOMPLISHMENTS ===
• Multi-Unit Scale & Revenue: Sustained 25% Sales Growth across 5 store locations (Wingstop). Mentored GMs and executed high-volume guest satisfaction initiatives.
• Inventory & Cost Control: Exceeded Cost of Sales targets for 24 Consecutive Periods (Pizza Hut), sustaining multi-year gross margin expansion across 8 locations.
• Turnover & Retention: Achieved a 28% Increase in employee retention (Church's Chicken), cutting manager turnover by 15-28% through structured onboarding.
• Custom Logistics Engineering: Designed and deployed a custom 'Build-to-Inventory' 1, 2, and 3-stop delivery scheduling algorithm, reducing food cost variance and waste.
• Labor Optimization: Streamlined scheduling workflows to achieve a 10% Reduction in labor expenses while raising customer satisfaction by 25%.

=== PROPRIETARY 3-LAYER OPERATIONAL INTELLIGENCE FRAMEWORK ===
Layer 1 — Verified Unit Baseline Audit:
  Conducts granular P&L, food cost, labor variance, and QSC safety compliance audits across all assigned units within 30 days.
Layer 2 — Leadership & Process Engineering:
  Deploys custom Build-to-Inventory delivery algorithms, streamlines labor scheduling, and institutes structured General Manager mentorship to eliminate manager burnout and turnover.
Layer 3 — Automated Governance & Margin Control:
  Establishes continuous audit frameworks and automated reporting controls to sustain long-term gross margin and EBITDA growth.

=== 90-DAY OPERATIONAL SCALING PLAYBOOK ===
• Days 1–30 (Diagnostic & Baseline Audit): Full financial & QSC operational audits of all store locations; establish baseline labor/cost-of-goods metrics.
• Days 31–60 (Process Alignment & GM Mentorship): Roll out Build-to-Inventory scheduling and labor optimization; implement GM coaching to stabilize staffing.
• Days 61–90 (Governance Lock & Margin Expansion): Lock in 24-period inventory cost control systems; deliver target +15-25% revenue growth and 10% labor savings.

=== EDUCATION & CERTIFICATIONS ===
• A.A.S. Computer Programming — Vatterott College, St. Louis, MO
• Six Sigma Yellow Belt Certification (In Progress)
• Master of Arts & Bachelor of Arts, Biblical Studies — Glad Tidings Bible College, St. Louis, MO`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(executiveBriefText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-3xl glass-panel p-6 rounded-2xl border border-slate-800 relative max-h-[90vh] overflow-y-auto custom-scrollbar">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div>
            <h3 className="text-lg font-bold text-white font-heading flex items-center gap-2">
              <Award className="w-5 h-5 text-amber-400" />
              Executive Portfolio Brief & 90-Day Scaling Playbook
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Donald Woods • 314-917-3503 • donaldwoods@live.com • Florissant, MO
            </p>
          </div>
          <button onClick={onClose} className="p-1 rounded bg-slate-800 text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Value Proposition Badge */}
        <div className="my-4 p-3.5 rounded-xl bg-sky-500/10 border border-sky-500/20 text-xs text-sky-300 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-sky-400 flex-shrink-0" />
            <span>
              <strong>Ready for Executive Presentation</strong>: Attach this brief to job applications or present it in interviews as your proprietary operational scaling framework.
            </span>
          </div>
          <button
            onClick={copyToClipboard}
            className="px-3 py-1.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-white text-xs font-semibold flex items-center gap-1.5 flex-shrink-0 ml-3"
          >
            {copied ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? "Copied Brief!" : "Copy Full Brief"}</span>
          </button>
        </div>

        {/* Text Area */}
        <textarea
          readOnly
          rows={16}
          value={executiveBriefText}
          className="w-full p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 leading-relaxed font-mono outline-none custom-scrollbar resize-none"
        />

        {/* Footer */}
        <div className="mt-5 pt-4 border-t border-slate-800 flex items-center justify-between">
          <span className="text-xs text-slate-400">
            Woods Leadership Framework v4.3 • 100% Grounded Career Evidence
          </span>
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};

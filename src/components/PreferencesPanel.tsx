'use client';

import React, { useState } from 'react';
import { Sliders, MapPin, DollarSign, Briefcase, Ban, Clock, ChevronDown, ChevronUp, Save, CheckCircle2 } from 'lucide-react';

export interface Preferences {
  targetRoles: string;
  location: string;
  distance: number;
  isRemote: boolean;
  minSalary: number;
  maxTravel: string;
  schedulePreference: string;
  excludedIndustries: string;
}

interface PreferencesPanelProps {
  preferences: Preferences;
  onSavePreferences: (prefs: Preferences) => void;
}

export const PreferencesPanel: React.FC<PreferencesPanelProps> = ({
  preferences,
  onSavePreferences,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [prefs, setPrefs] = useState<Preferences>(preferences);
  const [saved, setSaved] = useState(false);

  const handleChange = (key: keyof Preferences, value: any) => {
    setPrefs(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    onSavePreferences(prefs);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-800 mb-6 transition-all">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
          <div className="p-2 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
            <Sliders className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white font-heading flex items-center gap-2">
              Career Search Preferences & Practical Filters
              <span className="text-[11px] font-normal text-slate-400 font-sans">
                ({prefs.location} • ${prefs.minSalary.toLocaleString()}+ • {prefs.distance} miles)
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">
              Configure Florissant location radius, salary thresholds, schedule limits, and employer exclusions.
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
        >
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {isOpen && (
        <div className="mt-5 pt-4 border-t border-slate-800 space-y-4 animate-fadeIn">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Target Roles */}
            <div>
              <label className="text-xs font-semibold text-slate-300 mb-1 flex items-center gap-1.5">
                <Briefcase className="w-3.5 h-3.5 text-sky-400" />
                Target Roles Search Query
              </label>
              <input
                type="text"
                value={prefs.targetRoles}
                onChange={(e) => handleChange('targetRoles', e.target.value)}
                placeholder="e.g. Operations Manager OR Process Improvement Manager"
                className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500"
              />
            </div>

            {/* Location & Radius */}
            <div>
              <label className="text-xs font-semibold text-slate-300 mb-1 flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5 text-emerald-400" />
                Home Location & Radius (miles)
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={prefs.location}
                  onChange={(e) => handleChange('location', e.target.value)}
                  placeholder="Florissant, MO"
                  className="flex-1 px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500"
                />
                <select
                  value={prefs.distance}
                  onChange={(e) => handleChange('distance', Number(e.target.value))}
                  className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500"
                >
                  <option value={10}>10 miles</option>
                  <option value={25}>25 miles</option>
                  <option value={50}>50 miles</option>
                  <option value={100}>100 miles</option>
                </select>
              </div>
            </div>

            {/* Minimum Salary */}
            <div>
              <label className="text-xs font-semibold text-slate-300 mb-1 flex items-center gap-1.5">
                <DollarSign className="w-3.5 h-3.5 text-amber-400" />
                Minimum Salary Floor ($ USD)
              </label>
              <input
                type="number"
                step={5000}
                value={prefs.minSalary}
                onChange={(e) => handleChange('minSalary', Number(e.target.value))}
                placeholder="95000"
                className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500"
              />
            </div>

            {/* Schedule & Travel Limits */}
            <div>
              <label className="text-xs font-semibold text-slate-300 mb-1 flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-purple-400" />
                Schedule & Travel Limits
              </label>
              <input
                type="text"
                value={prefs.maxTravel}
                onChange={(e) => handleChange('maxTravel', e.target.value)}
                placeholder="Max 15% travel, Full-Time Day Shift"
                className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500"
              />
            </div>

            {/* Exclusion Filters */}
            <div className="md:col-span-2">
              <label className="text-xs font-semibold text-slate-300 mb-1 flex items-center gap-1.5">
                <Ban className="w-3.5 h-3.5 text-rose-400" />
                Excluded Industries or Employer Keywords
              </label>
              <input
                type="text"
                value={prefs.excludedIndustries}
                onChange={(e) => handleChange('excludedIndustries', e.target.value)}
                placeholder="Comma separated exclusions (e.g. Door-to-door sales, Multi-level marketing)"
                className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs outline-none focus:border-sky-500"
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-3 border-t border-slate-800/80">
            <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                checked={prefs.isRemote}
                onChange={(e) => handleChange('isRemote', e.target.checked)}
                className="w-4 h-4 rounded bg-slate-900 border-slate-700 text-sky-500 focus:ring-sky-500"
              />
              <span>Include Remote Roles Nationwide</span>
            </label>

            <div className="flex items-center gap-2">
              {saved && (
                <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Preferences Saved!
                </span>
              )}
              <button
                onClick={handleSave}
                className="px-4 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md shadow-sky-500/20"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Save Preferences</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

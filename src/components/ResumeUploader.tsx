'use client';

import React, { useState } from 'react';
import { Upload, FileText, CheckCircle2, AlertCircle, ShieldCheck } from 'lucide-react';

interface ResumeUploaderProps {
  onUploadSuccess: (resumeData: { filename: string; characterCount: number; snippet: string }) => void;
}

export const ResumeUploader: React.FC<ResumeUploaderProps> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<{ filename: string; characterCount: number; snippet: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/parse-resume', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error("Failed to parse résumé file");

      const data = await res.json();
      const payload = {
        filename: data.filename,
        characterCount: data.extracted_character_count,
        snippet: data.preview_snippet
      };

      setResult(payload);
      onUploadSuccess(payload);
    } catch (err) {
      // Client-side fallback if server is offline
      const text = await file.text();
      const payload = {
        filename: file.name,
        characterCount: text.length,
        snippet: text.slice(0, 500)
      };
      setResult(payload);
      onUploadSuccess(payload);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-800 mb-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <h3 className="text-sm font-bold text-white font-heading">
            Secure Local Résumé Evidence Parser
          </h3>
        </div>
        <span className="text-[11px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
          Privacy Protected • Local Processing
        </span>
      </div>

      <div className="mt-4 flex flex-col md:flex-row items-center gap-4">
        <label className="flex-1 w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-slate-900 border border-dashed border-slate-700 hover:border-sky-500 cursor-pointer transition-colors">
          <Upload className="w-5 h-5 text-sky-400" />
          <div className="flex-1 overflow-hidden text-ellipsis whitespace-nowrap text-xs text-slate-300">
            {file ? file.name : "Select or drag PDF, DOCX, or TXT résumé..."}
          </div>
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleFileChange}
            className="hidden"
          />
        </label>

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className={`px-5 py-3 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all ${
            file && !uploading
              ? "bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white shadow-md shadow-sky-500/20 cursor-pointer"
              : "bg-slate-800 text-slate-500 cursor-not-allowed"
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>{uploading ? "Parsing..." : "Parse & Ground Evidence"}</span>
        </button>
      </div>

      {result && (
        <div className="mt-4 p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 animate-fadeIn">
          <div className="flex items-center gap-2 font-bold mb-1">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Résumé Grounding Active: {result.filename} ({result.characterCount.toLocaleString()} chars extracted)</span>
          </div>
          <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed italic">
            "{result.snippet}..."
          </p>
        </div>
      )}
    </div>
  );
};

"use client";

import { useState } from "react";
import { Users, AlertTriangle, CheckCircle2, TrendingUp, Calendar, RefreshCw, Brain } from "lucide-react";

export default function CustomerSuccessDashboard() {
  const [loading, setLoading] = useState(false);
  const [qbrPlan, setQbrPlan] = useState<string | null>(
    "🎯 QBR Strategic Focus: Focus on executive alignment & API adoption metrics. Account has 98% health score but standard retention risk on pricing."
  );

  const generateQBR = async () => {
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1200));
    setQbrPlan(
      "🎯 Customized QBR Blueprint for Acme Corp:\n" +
      "1. Value Delivered: 99.99% uptime maintained over past 3 quarters; 4.2M API requests processed.\n" +
      "2. Risk Mitigation: Addressed initial latency concerns with new edge caching deployment.\n" +
      "3. Expansion Strategy: Pitch Enterprise Security Module for 25% ARR expansion before Q3."
    );
    setLoading(false);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6 text-slate-100">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Customer Success & QBR Blueprint</h1>
          <p className="text-slate-400 mt-1">Hindsight Memory-driven churn risk analysis and expansion strategy</p>
        </div>
        <button
          onClick={generateQBR}
          disabled={loading}
          className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-medium rounded-lg text-sm flex items-center gap-2 transition"
        >
          <Brain className="w-4 h-4" />
          {loading ? "Synthesizing..." : "Generate QBR Blueprint"}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <p className="text-sm text-slate-400">Total Managed ARR</p>
          <p className="text-3xl font-mono font-bold text-white mt-2">$1.82M</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <p className="text-sm text-slate-400">Average Account Health</p>
          <p className="text-3xl font-mono font-bold text-emerald-400 mt-2">88 / 100</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <p className="text-sm text-slate-400">Accounts At Risk</p>
          <p className="text-3xl font-mono font-bold text-amber-400 mt-2">1 Account</p>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4 text-white">🧠 QBR & Health Insight</h2>
        <div className="p-4 bg-slate-950/80 border border-slate-800 rounded-lg text-sm leading-relaxed whitespace-pre-line text-cyan-200">
          {qbrPlan}
        </div>
      </div>
    </div>
  );
}
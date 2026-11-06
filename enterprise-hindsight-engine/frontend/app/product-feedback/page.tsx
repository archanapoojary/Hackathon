"use client";

import { useState } from "react";
import { MessageSquare, ThumbsUp, Layers, Filter, RefreshCw, Brain } from "lucide-react";

export default function ProductFeedbackDashboard() {
  const [loading, setLoading] = useState(false);
  const [synthesis, setSynthesis] = useState<string | null>(
    "📊 Feature Request Synthesis:\n" +
    "1. API Latency & Edge Caching (Weighted Score: 94/100) — Tied to $430k active ARR. Top objection across Acme Corp & Globex.\n" +
    "2. SOC2 Compliance Reporting Automation (Weighted Score: 82/100) — Requested by 3 enterprise champions.\n" +
    "3. Custom Role-Based Access Control (Weighted Score: 65/100) — Security procurement requirement."
  );

  const synthesizeFeedback = async () => {
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1200));
    setSynthesis(
      "📊 Updated Memory-Weighted Feature Prioritization:\n" +
      "1. Edge Caching & Regional Latency Optimization — Impact: $680k Pipeline across 4 deals.\n" +
      "2. Automated SOC2 / HIPAA Audit Export — Impact: Unblocks Stark Industries deal ($500k ARR).\n" +
      "3. Real-time Memory Graph Visualization — Impact: Highly requested in PLG feedback surveys."
    );
    setLoading(false);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6 text-slate-100">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Weighted Feature Request Synthesizer</h1>
          <p className="text-slate-400 mt-1">Cross-referencing PLG feedback with deal ARR & objection graphs</p>
        </div>
        <button
          onClick={synthesizeFeedback}
          disabled={loading}
          className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-medium rounded-lg text-sm flex items-center gap-2 transition"
        >
          <Brain className="w-4 h-4" />
          {loading ? "Synthesizing..." : "Synthesize Feedback"}
        </button>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4 text-white">🧠 Product Feedback Intelligence</h2>
        <div className="p-4 bg-slate-950/80 border border-slate-800 rounded-lg text-sm leading-relaxed whitespace-pre-line text-cyan-200">
          {synthesis}
        </div>
      </div>
    </div>
  );
}
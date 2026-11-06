"use client";

import React from "react";
import { DollarSign, TrendingUp, Shield, Calendar, Users, AlertTriangle } from "lucide-react";

interface DealCardProps {
  deal: {
    id: string;
    name: string;
    company: string;
    stage: string;
    value: number;
    probability: number;
    champion: string;
    healthScore: number;
    status: "active" | "at-risk" | "won" | "lost";
    objections?: string[];
  };
  onClick?: () => void;
  selected?: boolean;
}

export function DealCard({ deal, onClick, selected }: DealCardProps) {
  const getHealthColor = (score: number) => {
    if (score >= 80) return "text-emerald-400";
    if (score >= 60) return "text-amber-400";
    return "text-rose-400";
  };

  return (
    <div
      onClick={onClick}
      className={`p-4 rounded-xl border cursor-pointer transition-all ${
        selected
          ? "bg-slate-800/80 border-cyan-500 shadow-lg shadow-cyan-500/10"
          : "bg-slate-900/50 border-slate-800 hover:border-slate-700 hover:bg-slate-800/40"
      }`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <h3 className="font-semibold text-white truncate">{deal.name}</h3>
        <span
          className={`px-2 py-0.5 text-xs font-medium rounded-full ${
            deal.status === "active"
              ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"
              : deal.status === "at-risk"
              ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
              : deal.status === "won"
              ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
              : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
          }`}
        >
          {deal.stage}
        </span>
      </div>
      <p className="text-sm text-slate-400 mb-3">{deal.company}</p>

      <div className="grid grid-cols-3 gap-2 text-xs py-2 border-y border-slate-800/60 mb-3">
        <div>
          <span className="text-slate-500 block">ARR</span>
          <span className="font-mono text-slate-200">${(deal.value / 1000).toFixed(0)}k</span>
        </div>
        <div>
          <span className="text-slate-500 block">Win Rate</span>
          <span className="font-mono text-slate-200">{deal.probability}%</span>
        </div>
        <div>
          <span className="text-slate-500 block">Health</span>
          <span className={`font-mono font-semibold ${getHealthColor(deal.healthScore)}`}>
            {deal.healthScore}
          </span>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center gap-1">
          <Users className="w-3.5 h-3.5 text-slate-500" />
          <span>{deal.champion}</span>
        </div>
        {deal.objections && deal.objections.length > 0 && (
          <div className="flex items-center gap-1 text-amber-400">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>{deal.objections.length} objections</span>
          </div>
        )}
      </div>
    </div>
  );
}
export default DealCard;
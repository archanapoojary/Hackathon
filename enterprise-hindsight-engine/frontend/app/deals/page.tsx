"use client";

import { useState, useEffect } from "react";
import {
  Target,
  AlertTriangle,
  TrendingUp,
  Users,
  Clock,
  RefreshCw,
  Brain,
  ChevronDown,
  ChevronUp,
  FileText,
  Phone,
  Mail,
  Calendar,
  DollarSign,
  Shield,
  Zap,
  Search,
  Filter,
  MoreHorizontal,
  Eye,
  Edit,
  Trash2,
  ArrowRight,
  Plus,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Deal {
  id: string;
  name: string;
  company: string;
  stage: string;
  value: number;
  arr: number;
  probability: number;
  champion: string;
  championRole: string;
  nextStep: string;
  nextStepDate: string;
  lastContact: string;
  interactions: number;
  healthScore: number;
  objections: string[];
  competitor: string | null;
  status: "active" | "at-risk" | "won" | "lost";
}

interface Briefing {
  id: string;
  dealId: string;
  summary: string;
  topObjections: string[];
  tacticalAdjustments: string[];
  openingQuestion: string;
  generatedAt: string;
}

const mockDeals: Deal[] = [
  {
    id: "deal-001",
    name: "Acme Corp - Enterprise License",
    company: "Acme Corporation",
    stage: "Technical Validation",
    value: 250000,
    arr: 250000,
    probability: 65,
    champion: "Sarah Jenkins",
    championRole: "VP Engineering",
    nextStep: "Technical deep-dive with security team",
    nextStepDate: "2024-01-15",
    lastContact: "2 days ago",
    interactions: 12,
    healthScore: 78,
    objections: ["API latency concerns", "Security compliance requirements", "Pricing vs. competitor"],
    competitor: "Datadog",
    status: "active",
  },
  {
    id: "deal-002",
    name: "Globex - Platform Migration",
    company: "Globex International",
    stage: "Negotiation",
    value: 180000,
    arr: 180000,
    probability: 45,
    champion: "Marcus Chen",
    championRole: "CTO",
    nextStep: "Procurement review & legal redlines",
    nextStepDate: "2024-01-18",
    lastContact: "5 days ago",
    interactions: 8,
    healthScore: 62,
    objections: ["Migration complexity", "Data sovereignty", "Contract terms"],
    competitor: "New Relic",
    status: "at-risk",
  },
  {
    id: "deal-003",
    name: "Stark Industries - Expansion",
    company: "Stark Industries",
    stage: "Discovery",
    value: 500000,
    arr: 500000,
    probability: 30,
    champion: "Pepper Potts",
    championRole: "CEO",
    nextStep: "Executive alignment workshop",
    nextStepDate: "2024-01-22",
    lastContact: "1 day ago",
    interactions: 4,
    healthScore: 85,
    objections: ["Budget approval timeline", "Integration with legacy systems"],
    competitor: null,
    status: "active",
  },
  {
    id: "deal-004",
    name: "Wayne Enterprises - Security Suite",
    company: "Wayne Enterprises",
    stage: "Proof of Concept",
    value: 320000,
    arr: 320000,
    probability: 70,
    champion: "Lucius Fox",
    championRole: "CTO",
    nextStep: "POC results presentation",
    nextStepDate: "2024-01-10",
    lastContact: "3 hours ago",
    interactions: 15,
    healthScore: 91,
    objections: ["Performance at scale", "Custom compliance requirements"],
    competitor: "Splunk",
    status: "active",
  },
  {
    id: "deal-005",
    name: "Umbrella Corp - Renewal & Upsell",
    company: "Umbrella Corporation",
    stage: "Renewal",
    value: 150000,
    arr: 150000,
    probability: 90,
    champion: "Albert Wesker",
    championRole: "VP IT",
    nextStep: "Renewal signature",
    nextStepDate: "2024-01-08",
    lastContact: "1 week ago",
    interactions: 6,
    healthScore: 95,
    objections: [],
    competitor: null,
    status: "active",
  },
];

const mockBriefing: Briefing = {
  id: "brief-001",
  dealId: "deal-001",
  summary: "Acme Corp is in Technical Validation with strong champion engagement. Historical memory shows CTO previously raised API latency concerns 14 days ago during Discovery call. Security compliance was resolved in Call 3 but procurement will likely push on pricing.",
  topObjections: [
    "API latency concerns (raised by CTO in Call 2) — pitch new edge caching update immediately",
    "Security compliance (resolved in Call 3 but procurement will re-verify) — have SOC2 Type II ready",
    "Pricing vs. Datadog (procurement benchmark) — anchor on TCO savings from consolidation",
  ],
  tacticalAdjustments: [
    "Lead with edge caching performance demo — addresses #1 historical objection",
    "Bring security engineer to next call — pre-empts procurement compliance questions",
    "Prepare competitive displacement deck — Datadog pricing comparison with 40% TCO savings",
    "Avoid standard pricing talk until security compliance is confirmed by procurement",
  ],
  openingQuestion: "Sarah, last time we spoke your CTO was concerned about API latency at scale — want to show you how our new edge caching layer cuts p99 latency by 60%?",
  generatedAt: "2024-01-10T14:32:00Z",
};

const stages = [
  "Discovery",
  "Technical Validation",
  "Proof of Concept",
  "Negotiation",
  "Procurement",
  "Closed Won",
  "Closed Lost",
];

const statusColors = {
  active: "badge-info",
  "at-risk": "badge-warning",
  won: "badge-success",
  lost: "badge-error",
};

const stageColors = {
  Discovery: "badge-info",
  "Technical Validation": "badge-info",
  "Proof of Concept": "badge-warning",
  Negotiation: "badge-warning",
  Procurement: "badge-warning",
  "Closed Won": "badge-success",
  "Closed Lost": "badge-error",
};

export default function DealIntelligenceDashboard() {
  const [deals] = useState<Deal[]>(mockDeals);
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(deals[0]);
  const [briefing, setBriefing] = useState<Briefing>(mockBriefing);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [stageFilter, setStageFilter] = useState<string>("all");
  const [showBriefing, setShowBriefing] = useState(true);

  const filteredDeals = deals.filter((deal) => {
    const matchesSearch =
      deal.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      deal.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      deal.champion.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStage = stageFilter === "all" || deal.stage === stageFilter;
    return matchesSearch && matchesStage;
  });

  const totalPipeline = deals.reduce((sum, d) => sum + d.value * (d.probability / 100), 0);
  const totalARR = deals.reduce((sum, d) => sum + d.arr, 0);
  const activeDeals = deals.filter((d) => d.status === "active").length;
  const atRiskDeals = deals.filter((d) => d.status === "at-risk").length;

  const generateBriefing = async () => {
    if (!selectedDeal) return;
    setGenerating(true);
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));
    setBriefing({
      ...mockBriefing,
      dealId: selectedDeal.id,
      generatedAt: new Date().toISOString(),
    });
    setGenerating(false);
  };

  const getHealthColor = (score: number) => {
    if (score >= 80) return "text-accent-emerald";
    if (score >= 60) return "text-accent-amber";
    return "text-accent-rose";
  };

  return (
    <div className="flex min-h-screen bg-background">
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Bar */}
        <header className="h-16 bg-surface/80 backdrop-blur-md border-b border-border sticky top-0 z-40">
          <div className="flex h-full items-center justify-between px-4 md:px-6">
            <div className="flex items-center gap-3">
              <Target className="w-6 h-6 text-accent-cyan" />
              <div>
                <h1 className="text-heading-lg font-semibold text-text-PRIMARY">Deal Intelligence</h1>
                <p className="text-body-xs text-text-secondary">Pre-call briefings & objection evolution powered by Hindsight memory</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={generateBriefing}
                disabled={generating || !selectedDeal}
                className="btn-primary"
              >
                <Brain className="w-4 h-4" />
                {generating ? "Generating..." : "Generate AI Briefing"}
              </button>
              <button className="btn-secondary">
                <Plus className="w-4 h-4" />
                New Deal
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          <div className="page-container">
            {/* Pipeline Summary */}
            <section className="mb-8 animate-slide-up">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="card-elevated p-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-caption text-text-secondary">Active Deals</p>
                      <p className="text-display-sm font-mono font-semibold text-text-PRIMARY mt-1">{activeDeals}</p>
                    </div>
                    <div className="p-2 rounded-radius-md bg-accent-cyan/15">
                      <Target className="w-5 h-5 text-accent-cyan" />
                    </div>
                  </div>
                </div>
                <div className="card-elevated p-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-caption text-text-secondary">Weighted Pipeline</p>
                      <p className="text-display-sm font-mono font-semibold text-text-PRIMARY mt-1">${(totalPipeline / 1000000).toFixed(1)}M</p>
                    </div>
                    <div className="p-2 rounded-radius-md bg-accent-emerald/15">
                      <TrendingUp className="w-5 h-5 text-accent-emerald" />
                    </div>
                  </div>
                </div>
                <div className="card-elevated p-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-caption text-text-secondary">Total ARR</p>
                      <p className="text-display-sm font-mono font-semibold text-text-PRIMARY mt-1">${(totalARR / 1000000).toFixed(1)}M</p>
                    </div>
                    <div className="p-2 rounded-radius-md bg-accent-amber/15">
                      <DollarSign className="w-5 h-5 text-accent-amber" />
                    </div>
                  </div>
                </div>
                <div className="card-elevated p-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-caption text-text-secondary">At Risk</p>
                      <p className="text-display-sm font-mono font-semibold text-accent-rose mt-1">{atRiskDeals}</p>
                    </div>
                    <div className="p-2 rounded-radius-md bg-accent-rose/15">
                      <AlertTriangle className="w-5 h-5 text-accent-rose" />
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Main Grid */}
            <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Deal List */}
              <div className="lg:col-span-1 animate-slide-up">
                <div className="card-elevated overflow-hidden">
                  <div className="p-4 border-b border-border flex items-center justify-between">
                    <h2 className="text-heading-md font-semibold">Deal Pipeline</h2>
                    <button className="btn-ghost btn-sm p-2">
                      <Filter className="w-4 h-4" />
                    </button>
                  </div>

                  {/* Search & Filter */}
                  <div className="p-4 border-b border-border space-y-3">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
                      <input
                        type="text"
                        placeholder="Search deals..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="input pl-10"
                      />
                    </div>
                    <select
                      value={stageFilter}
                      onChange={(e) => setStageFilter(e.target.value)}
                      className="input"
                    >
                      <option value="all">All Stages</option>
                      {stages.map((stage) => (
                        <option key={stage} value={stage}>
                          {stage}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Deal List */}
                  <div className="max-h-[600px] overflow-y-auto">
                    {filteredDeals.length === 0 ? (
                      <div className="p-8 text-center text-text-muted">
                        <Target className="w-12 h-12 mx-auto mb-3 opacity-50" />
                        <p className="text-body-sm">No deals match your filters</p>
                      </div>
                    ) : (
                      <ul className="divide-y divide-border" role="list">
                        {filteredDeals.map((deal) => (
                          <li key={deal.id}>
                            <button
                              onClick={() => {
                                setSelectedDeal(deal);
                                setShowBriefing(true);
                              }}
                              className={cn(
                                "w-full p-4 text-left hover:bg-surface-elevated/50 transition-colors flex items-start gap-3",
                                selectedDeal?.id === deal.id && "bg-accent-cyan/5 border-l-2 border-accent-cyan"
                              )}
                            >
                              <div className="flex-1 min-w-0">
                                <div className="flex items-start justify-between gap-2">
                                  <h3 className="text-body-sm font-medium text-text-PRIMARY truncate">{deal.name}</h3>
                                  <span className={cn("badge", stageColors[deal.stage as keyof typeof stageColors])}>
                                    {deal.stage}
                                  </span>
                                </div>
                                <p className="text-body-xs text-text-secondary mt-0.5 truncate">{deal.company}</p>
                                <div className="flex items-center gap-3 mt-2 text-body-xs text-text-muted">
                                  <span className="flex items-center gap-1">
                                    <DollarSign className="w-3 h-3" />
                                    ${(deal.value / 1000).toFixed(0)}k
                                  </span>
                                  <span className="flex items-center gap-1">
                                    <TrendingUp className="w-3 h-3" />
                                    {deal.probability}%
                                  </span>
                                  <span className={cn("flex items-center gap-1", getHealthColor(deal.healthScore))}>
                                    <Shield className="w-3 h-3" />
                                    {deal.healthScore}
                                  </span>
                                </div>
                              </div>
                              <span className={cn("badge", statusColors[deal.status])}>{deal.status}</span>
                            </button>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              </div>

              {/* Deal Detail + Briefing */}
              <div className="lg:col-span-2 space-y-6">
                {selectedDeal && (
                  <>
                    {/* Deal Detail Card */}
                    <div className="card-elevated animate-slide-up">
                      <div className="p-6 border-b border-border">
                        <div className="flex flex-wrap items-start justify-between gap-4">
                          <div>
                            <div className="flex items-center gap-2 mb-2">
                              <h2 className="text-heading-lg font-semibold text-text-PRIMARY">{selectedDeal.name}</h2>
                              <span className={cn("badge", stageColors[selectedDeal.stage as keyof typeof stageColors])}>
                                {selectedDeal.stage}
                              </span>
                              <span className={cn("badge", statusColors[selectedDeal.status])}>
                                {selectedDeal.status}
                              </span>
                            </div>
                            <p className="text-body-md text-text-secondary">{selectedDeal.company}</p>
                          </div>
                          <div className="flex items-center gap-2">
                            <button className="btn-secondary btn-sm">
                              <Phone className="w-3.5 h-3.5" />
                              Call
                            </button>
                            <button className="btn-secondary btn-sm">
                              <Mail className="w-3.5 h-3.5" />
                              Email
                            </button>
                            <button className="btn-secondary btn-sm">
                              <Calendar className="w-3.5 h-3.5" />
                              Schedule
                            </button>
                          </div>
                        </div>
                      </div>

                      <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Key Metrics */}
                        <div className="space-y-4">
                          <div>
                            <p className="text-caption text-text-secondary">Deal Value</p>
                            <p className="text-display-sm font-mono font-semibold text-text-PRIMARY">${(selectedDeal.value / 1000).toFixed(0)}k</p>
                          </div>
                          <div>
                            <p className="text-caption text-text-secondary">ARR</p>
                            <p className="text-display-sm font-mono font-semibold text-text-PRIMARY">${(selectedDeal.arr / 1000).toFixed(0)}k</p>
                          </div>
                          <div>
                            <p className="text-caption text-text-secondary">Win Probability</p>
                            <p className="text-display-sm font-mono font-semibold text-accent-emerald">{selectedDeal.probability}%</p>
                          </div>
                          <div>
                            <p className="text-caption text-text-secondary">Health Score</p>
                            <div className="flex items-center gap-2">
                              <div className="flex-1 h-2 bg-surface-elevated rounded-radius-full overflow-hidden">
                                <div
                                  className="h-full bg-accent-emerald rounded-radius-full transition-all duration-500"
                                  style={{ width: `${selectedDeal.healthScore}%` }}
                                />
                              </div>
                              <span className={cn("text-body-sm font-mono font-semibold", getHealthColor(selectedDeal.healthScore))}>
                                {selectedDeal.healthScore}
                              </span>
                            </div>
                          </div>
                        </div>

                        {/* Champion & Next Steps */}
                        <div className="md:col-span-2 space-y-4">
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div className="card p-4">
                              <p className="text-caption text-text-secondary">Champion</p>
                              <div className="flex items-center gap-3 mt-2">
                                <div className="w-10 h-10 rounded-radius-full bg-accent-cyan/15 flex items-center justify-center">
                                  <Users className="w-5 h-5 text-accent-cyan" />
                                </div>
                                <div>
                                  <p className="text-body-md font-medium text-text-PRIMARY">{selectedDeal.champion}</p>
                                  <p className="text-body-sm text-text-secondary">{selectedDeal.championRole}</p>
                                </div>
                              </div>
                            </div>
                            <div className="card p-4">
                              <p className="text-caption text-text-secondary">Competitor</p>
                              <p className="text-body-md font-medium text-text-PRIMARY mt-2">
                                {selectedDeal.competitor || "None identified"}
                              </p>
                            </div>
                            <div className="card p-4">
                              <p className="text-caption text-text-secondary">Next Step</p>
                              <p className="text-body-md font-medium text-text-PRIMARY mt-2">{selectedDeal.nextStep}</p>
                              <p className="text-body-xs text-text-secondary mt-1">
                                <Calendar className="w-3 h-3 inline-block align-middle mr-1" />
                                {selectedDeal.nextStepDate}
                              </p>
                            </div>
                            <div className="card p-4">
                              <p className="text-caption text-text-secondary">Last Contact</p>
                              <p className="text-body-md font-medium text-text-PRIMARY mt-2">{selectedDeal.lastContact}</p>
                              <p className="text-body-xs text-text-secondary mt-1">
                                <Clock className="w-3 h-3 inline-block align-middle mr-1" />
                                {selectedDeal.interactions} interactions logged
                              </p>
                            </div>
                          </div>

                          {/* Objections */}
                          {selectedDeal.objections.length > 0 && (
                            <div className="card p-4 border-border/50">
                              <div className="flex items-center justify-between mb-3">
                                <p className="text-caption text-text-secondary">Active Objections</p>
                                <Brain className="w-4 h-4 text-accent-cyan" />
                              </div>
                              <div className="flex flex-wrap gap-2">
                                {selectedDeal.objections.map((objection, idx) => (
                                  <span key={idx} className="badge badge-warning">
                                    {objection}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Hindsight Briefing */}
                    {showBriefing && (
                      <div className="card-elevated animate-slide-up delay-100">
                        <div className="p-6 border-b border-border flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className="p-2 rounded-radius-md bg-accent-cyan/15">
                              <Brain className="w-5 h-5 text-accent-cyan" />
                            </div>
                            <div>
                              <h2 className="text-heading-lg font-semibold text-text-PRIMARY">Hindsight Strategic Briefing</h2>
                              <p className="text-body-xs text-text-secondary">
                                Generated {formatRelativeTime(briefing.generatedAt)} • Deal: {selectedDeal.name}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <button className="btn-ghost btn-sm" onClick={() => setShowBriefing(false)}>
                              <ChevronUp className="w-4 h-4" />
                              Collapse
                            </button>
                            <button
                              onClick={generateBriefing}
                              disabled={generating}
                              className="btn-primary btn-sm"
                            >
                              <RefreshCw className={cn("w-4 h-4", generating && "animate-spin")} />
                              Refresh
                            </button>
                          </div>
                        </div>

                        <div className="p-6 space-y-6">
                          {/* Summary */}
                          <div className="bg-surface/50 p-4 rounded-radius-md border border-border/50">
                            <h3 className="text-heading-sm font-semibold text-text-PRIMARY mb-2">Executive Summary</h3>
                            <p className="text-body-sm text-text-secondary leading-relaxed">{briefing.summary}</p>
                          </div>

                          {/* Top Objections */}
                          <div>
                            <h3 className="text-heading-sm font-semibold text-text-PRIMARY mb-3 flex items-center gap-2">
                              <AlertTriangle className="w-4 h-4 text-accent-amber" />
                              Top Historical Objections to Watch
                            </h3>
                            <div className="space-y-2">
                              {briefing.topObjections.map((objection, idx) => (
                                <div key={idx} className="card p-4 border-l-2 border-accent-amber">
                                  <p className="text-body-sm text-text-secondary">{objection}</p>
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Tactical Adjustments */}
                          <div>
                            <h3 className="text-heading-sm font-semibold text-text-PRIMARY mb-3 flex items-center gap-2">
                              <Zap className="w-4 h-4 text-accent-cyan" />
                              Winning Tactical Adjustments
                            </h3>
                            <div className="space-y-2">
                              {briefing.tacticalAdjustments.map((adjustment, idx) => (
                                <div key={idx} className="card p-4 border-l-2 border-accent-cyan">
                                  <p className="text-body-sm text-text-secondary">{adjustment}</p>
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Opening Question */}
                          <div className="bg-gradient-to-r from-accent-cyan/10 to-accent-emerald/10 p-6 rounded-radius-lg border border-accent-cyan/20">
                            <h3 className="text-heading-sm font-semibold text-text-PRIMARY mb-3 flex items-center gap-2">
                              <ArrowRight className="w-4 h-4 text-accent-cyan" />
                              Suggested Opening Question
                            </h3>
                            <p className="text-body-md text-text-PRIMARY font-medium italic leading-relaxed">
                              "{briefing.openingQuestion}"
                            </p>
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                )}

                {(!selectedDeal || !showBriefing) && (
                  <div className="card-elevated animate-slide-up">
                    <div className="p-12 text-center">
                      <Brain className="w-16 h-16 mx-auto mb-4 text-accent-cyan/50" />
                      <h3 className="text-heading-lg font-semibold text-text-PRIMARY mb-2">
                        {selectedDeal ? "Briefing Collapsed" : "Select a Deal"}
                      </h3>
                      <p className="text-body-md text-text-secondary max-w-md mx-auto">
                        {selectedDeal
                          ? "Click 'Generate AI Briefing' to get Hindsight-powered strategic advice for this deal."
                          : "Choose a deal from the pipeline to view details and generate a pre-call briefing."}
                      </p>
                      {selectedDeal && (
                        <button
                          onClick={generateBriefing}
                          disabled={generating}
                          className="btn-primary mt-4"
                        >
                          <Brain className="w-4 h-4" />
                          {generating ? "Generating..." : "Generate AI Briefing"}
                        </button>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}

// Re-use formatRelativeTime from utils
function formatRelativeTime(date: string): string {
  const now = new Date();
  const then = new Date(date);
  const diffMs = now.getTime() - then.getTime();
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffSecs < 60) return "just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return then.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}
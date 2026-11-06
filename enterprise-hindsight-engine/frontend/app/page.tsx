"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import {
  LayoutDashboard,
  Target,
  Users,
  MessageSquare,
  Brain,
  Zap,
  Shield,
  BarChart3,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Clock,
  ArrowRight,
  RefreshCw,
  Settings,
  HelpCircle,
} from "lucide-react";

const navigation = [
  { name: "Executive Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Deal Intelligence", href: "/deals", icon: Target },
  { name: "Customer Success", href: "/customer-success", icon: Users },
  { name: "Product Feedback", href: "/product-feedback", icon: MessageSquare },
];

const stats = [
  {
    label: "Active Deals",
    value: "24",
    change: "+3 this week",
    trend: "up",
    icon: Target,
    color: "cyan",
  },
  {
    label: "Pipeline Value",
    value: "$4.2M",
    change: "+12% MoM",
    trend: "up",
    icon: TrendingUp,
    color: "emerald",
  },
  {
    label: "At-Risk Accounts",
    value: "3",
    change: "-1 resolved",
    trend: "down",
    icon: AlertTriangle,
    color: "amber",
  },
  {
    label: "Memory Sync",
    value: "98.7%",
    change: "2.1s avg latency",
    trend: "up",
    icon: Brain,
    color: "cyan",
  },
];

const recentActivity = [
  {
    id: 1,
    type: "deal",
    title: "Acme Corp - Technical Validation",
    description: "CTO raised API latency concerns. Hindsight suggests edge caching pitch.",
    timestamp: "2 min ago",
    status: "warning",
  },
  {
    id: 2,
    type: "account",
    title: "Globex Health Score Drop",
    description: "Health score dropped from 87 to 72. Usage decline detected in analytics module.",
    timestamp: "15 min ago",
    status: "error",
  },
  {
    id: 3,
    type: "feedback",
    title: "Feature Request: SSO Integration",
    description: "3 enterprise accounts requested SAML/SSO. Weighted score: 94/100.",
    timestamp: "1 hour ago",
    status: "info",
  },
  {
    id: 4,
    type: "deal",
    title: "Stark Industries - Negotiation",
    description: "Procurement pushed back on pricing. Historical data shows 40% win rate at current tier.",
    timestamp: "3 hours ago",
    status: "info",
  },
  {
    id: 5,
    type: "sync",
    title: "Hindsight Memory Sync Complete",
    description: "127 new interactions indexed across 18 accounts. Zero conflicts detected.",
    timestamp: "6 hours ago",
    status: "success",
  },
];

const quickActions = [
  {
    label: "Generate Pre-Call Brief",
    description: "AI-powered briefing for upcoming calls",
    icon: Zap,
    href: "/deals?action=briefing",
    color: "cyan",
  },
  {
    label: "Run Churn Risk Analysis",
    description: "Scan all accounts for health signals",
    icon: Shield,
    href: "/customer-success?action=churn",
    color: "emerald",
  },
  {
    label: "Synthesize Feedback",
    description: "Weighted feature prioritization report",
    icon: BarChart3,
    href: "/product-feedback?action=synthesize",
    color: "amber",
  },
  {
    label: "Sync Memory Pipeline",
    description: "Manual trigger for Hindsight sync",
    icon: RefreshCw,
    href: "/settings?action=sync",
    color: "cyan",
  },
];

export default function ExecutiveDashboard() {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const getStatusStyles = (status: string) => {
    switch (status) {
      case "success":
        return "badge-success";
      case "warning":
        return "badge-warning";
      case "error":
        return "badge-error";
      case "info":
      default:
        return "badge-info";
    }
  };

  const getIconColor = (color: string) => {
    switch (color) {
      case "cyan":
        return "text-accent-cyan";
      case "emerald":
        return "text-accent-emerald";
      case "amber":
        return "text-accent-amber";
      default:
        return "text-accent-cyan";
    }
  };

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar
        navigation={navigation}
        pathname={pathname}
        open={sidebarOpen}
        onToggle={setSidebarOpen}
      />

      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Bar */}
        <header className="h-16 bg-surface/80 backdrop-blur-md border-b border-border sticky top-0 z-40">
          <div className="flex h-full items-center justify-between px-4 md:px-6">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="btn-ghost p-2 lg:hidden"
                aria-label="Toggle sidebar"
              >
                <LayoutDashboard className="w-5 h-5" />
              </button>
              <div className="hidden lg:flex items-center gap-2">
                <Brain className="w-6 h-6 text-accent-cyan" />
                <span className="text-heading-lg font-semibold text-text-PRIMARY">Hindsight Engine</span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-surface-elevated border border-border rounded-radius-full">
                <span className="status-dot status-dot-success status-dot-pulse" />
                <span className="text-body-xs text-text-secondary font-mono">Memory Online</span>
              </div>

              <div className="flex items-center gap-2">
                <button className="btn-ghost p-2" aria-label="Notifications">
                  <Bell className="w-5 h-5" />
                </button>
                <button className="btn-ghost p-2" aria-label="Settings">
                  <Settings className="w-5 h-5" />
                </button>
                <button className="btn-ghost p-2" aria-label="Help">
                  <HelpCircle className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          <div className="page-container">
            {/* Hero Section */}
            <section className="relative mb-8 md:mb-10 animate-slide-up">
              <div className="absolute inset-0 beam-backdrop-cyan" aria-hidden="true" />
              <div className="relative">
                <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-6">
                  <div>
                    <p className="text-caption text-accent-cyan mb-2">EXECUTIVE COMMAND CENTER</p>
                    <h1 className="text-display-md font-semibold text-text-PRIMARY">
                      Revenue Intelligence Overview
                    </h1>
                    <p className="text-body-md text-text-secondary mt-2 max-w-2xl">
                      Real-time deal intelligence, customer health, and product feedback synthesis
                      powered by persistent Hindsight memory and Groq inference.
                    </p>
                  </div>
                  <div className="flex items-center gap-3 pt-4 border-t border-border sm:pt-0 sm:border-t-0 sm:border-l sm:pl-6">
                    <div className="text-right">
                      <p className="text-display-sm font-mono font-semibold text-text-PRIMARY">98.7%</p>
                      <p className="text-caption text-text-secondary">Memory Sync Health</p>
                    </div>
                    <div className="w-px h-12 bg-border hidden sm:block" />
                    <div className="text-right">
                      <p className="text-display-sm font-mono font-semibold text-accent-emerald">2.1s</p>
                      <p className="text-caption text-text-secondary">Avg Recall Latency</p>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Key Metrics Grid */}
            <section className="mb-8 md:mb-10 animate-slide-up delay-100">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
                {stats.map((stat, index) => {
                  const Icon = stat.icon;
                  return (
                    <div
                      key={stat.label}
                      className="card-elevated p-6 animate-slide-up"
                      style={{ animationDelay: `${100 + index * 50}ms` }}
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className={`p-2 rounded-radius-md bg-accent-${stat.color}/15`}>
                          <Icon className={`w-5 h-5 ${getIconColor(stat.color)}`} aria-hidden="true" />
                        </div>
                        <span className={`badge ${stat.trend === "up" ? "badge-success" : "badge-warning"}`}>
                          {stat.trend === "up" ? (
                            <>
                              <TrendingUp className="w-3 h-3" /> {stat.change}
                            </>
                          ) : (
                            <>
                              <TrendingUp className="w-3 h-3 rotate-180" /> {stat.change}
                            </>
                          )}
                        </span>
                      </div>
                      <p className="text-caption text-text-secondary mb-1">{stat.label}</p>
                      <p className="text-display-sm font-mono font-semibold text-text-PRIMARY">{stat.value}</p>
                    </div>
                  );
                })}
              </div>
            </section>

            {/* Main Grid: Recent Activity + Quick Actions */}
            <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-slide-up delay-200">
              {/* Recent Activity */}
              <div className="lg:col-span-2">
                <div className="card-elevated overflow-hidden">
                  <div className="p-6 border-b border-border flex items-center justify-between">
                    <h2 className="text-heading-lg font-semibold">Recent Intelligence Activity</h2>
                    <Link
                      href="/activity"
                      className="btn-ghost text-body-sm"
                    >
                      View All <ArrowRight className="w-4 h-4" />
                    </Link>
                  </div>
                  <div className="divide-y divide-border">
                    {recentActivity.map((activity) => (
                      <div
                        key={activity.id}
                        className="p-6 hover:bg-surface-elevated/50 transition-colors flex items-start gap-4"
                      >
                        <div
                          className={`p-2 rounded-radius-md flex-shrink-0 ${
                            activity.status === "success"
                              ? "bg-accent-emerald/15 text-accent-emerald"
                              : activity.status === "warning"
                              ? "bg-accent-amber/15 text-accent-amber"
                              : activity.status === "error"
                              ? "bg-accent-rose/15 text-accent-rose"
                              : "bg-accent-cyan/15 text-accent-cyan"
                          }`}
                        >
                          {activity.type === "deal" && <Target className="w-5 h-5" />}
                          {activity.type === "account" && <Users className="w-5 h-5" />}
                          {activity.type === "feedback" && <MessageSquare className="w-5 h-5" />}
                          {activity.type === "sync" && <Brain className="w-5 h-5" />}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2">
                            <h3 className="text-body-md font-medium text-text-PRIMARY">{activity.title}</h3>
                            <span className="text-caption text-text-muted font-mono whitespace-nowrap">
                              {activity.timestamp}
                            </span>
                          </div>
                          <p className="text-body-sm text-text-secondary mt-1">{activity.description}</p>
                        </div>
                        <span className={getStatusStyles(activity.status)}>{activity.status}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="space-y-4">
                <h2 className="text-heading-lg font-semibold">Quick Actions</h2>
                <div className="space-y-3">
                  {quickActions.map((action, index) => {
                    const Icon = action.icon;
                    return (
                      <Link
                        key={action.label}
                        href={action.href}
                        className="card-interactive p-4 flex items-center gap-4 group animate-slide-up"
                        style={{ animationDelay: `${200 + index * 50}ms` }}
                      >
                        <div
                          className={`p-3 rounded-radius-lg flex-shrink-0 transition-colors ${
                            action.color === "cyan"
                              ? "bg-accent-cyan/15 text-accent-cyan group-hover:bg-accent-cyan/25"
                              : action.color === "emerald"
                              ? "bg-accent-emerald/15 text-accent-emerald group-hover:bg-accent-emerald/25"
                              : "bg-accent-amber/15 text-accent-amber group-hover:bg-accent-amber/25"
                          }`}
                        >
                          <Icon className="w-5 h-5" aria-hidden="true" />
                        </div>
                        <div className="flex-1 text-left">
                          <p className="text-body-sm font-medium text-text-PRIMARY group-hover:text-accent-cyan transition-colors">
                            {action.label}
                          </p>
                          <p className="text-body-xs text-text-secondary mt-0.5">{action.description}</p>
                        </div>
                        <ArrowRight className="w-4 h-4 text-text-muted group-hover:text-accent-cyan transition-colors" />
                      </Link>
                    );
                  })}
                </div>
              </div>
            </section>

            {/* System Status Footer */}
            <section className="mt-8 md:mt-10 animate-slide-up delay-300">
              <div className="card p-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-radius-md bg-accent-emerald/15">
                      <CheckCircle2 className="w-5 h-5 text-accent-emerald" />
                    </div>
                    <div>
                      <p className="text-body-sm font-medium text-text-PRIMARY">Hindsight Memory</p>
                      <p className="text-body-xs text-text-secondary">Connected • 184 accounts synced</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-radius-md bg-accent-cyan/15">
                      <Zap className="w-5 h-5 text-accent-cyan" />
                    </div>
                    <div>
                      <p className="text-body-sm font-medium text-text-PRIMARY">Groq Inference</p>
                      <p className="text-body-xs text-text-secondary">qwen/qwen3-32b • 247ms avg</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-radius-md bg-accent-emerald/15">
                      <Shield className="w-5 h-5 text-accent-emerald" />
                    </div>
                    <div>
                      <p className="text-body-sm font-medium text-text-PRIMARY">PostgreSQL</p>
                      <p className="text-body-xs text-text-secondary">Primary • 12ms p99 latency</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-radius-md bg-accent-cyan/15">
                      <Clock className="w-5 h-5 text-accent-cyan" />
                    </div>
                    <div>
                      <p className="text-body-sm font-medium text-text-PRIMARY">Memory Pipeline</p>
                      <p className="text-body-xs text-text-secondary">Last sync: 2 min ago</p>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}

// Bell icon component (inline to avoid extra import)
function Bell({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
    </svg>
  );
}
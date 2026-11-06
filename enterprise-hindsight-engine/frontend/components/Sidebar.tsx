"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Target,
  Users,
  MessageSquare,
  Brain,
  ChevronLeft,
  ChevronRight,
  Brain as BrainIcon,
  Zap,
  Shield,
  BarChart3,
  Settings,
  HelpCircle,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
  badgeColor?: "success" | "warning" | "error" | "info";
}

interface SidebarProps {
  navigation: NavItem[];
  pathname: string;
  open: boolean;
  onToggle: (open: boolean) => void;
}

const BADGE_COLORS = {
  success: "badge-success",
  warning: "badge-warning",
  error: "badge-error",
  info: "badge-info",
};

export default function Sidebar({
  navigation,
  pathname,
  open,
  onToggle,
}: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Sync collapsed state with open prop on mobile
  useEffect(() => {
    if (typeof window !== "undefined") {
      const isMobile = window.innerWidth < 1024;
      if (isMobile && !open) {
        setCollapsed(true);
      }
    }
  }, [open]);

  const handleToggleCollapse = () => {
    setCollapsed(!collapsed);
  };

  if (!mounted) {
    return (
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 bg-surface border-r border-border transition-all duration-normal",
          open ? "w-64" : "w-0 overflow-hidden"
        )}
        aria-label="Sidebar navigation"
      />
    );
  }

  const isMobile = typeof window !== "undefined" && window.innerWidth < 1024;

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-50 bg-surface border-r border-border transition-all duration-normal flex flex-col",
        isMobile
          ? open
            ? "w-64 shadow-xl"
            : "w-0 overflow-hidden"
          : collapsed
          ? "w-20"
          : "w-64"
      )}
      aria-label="Sidebar navigation"
      data-state={isMobile ? (open ? "open" : "closed") : collapsed ? "collapsed" : "expanded"}
    >
      {/* Logo / Brand */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-border">
        {!collapsed && (
          <Link href="/" className="flex items-center gap-2" aria-label="Hindsight Engine Home">
            <BrainIcon className="w-6 h-6 text-accent-cyan" aria-hidden="true" />
            <span className="text-heading-lg font-semibold text-text-PRIMARY">Hindsight Engine</span>
          </Link>
        )}
        <button
          onClick={handleToggleCollapse}
          className={cn(
            "btn-ghost p-1.5 rounded-radius-md transition-transform",
            collapsed && "rotate-180"
          )}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          aria-expanded={!collapsed}
        >
          {collapsed ? (
            <ChevronRight className="w-5 h-5" />
          ) : (
            <ChevronLeft className="w-5 h-5" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-1" aria-label="Main navigation">
        <div className="px-3 py-2 text-caption text-text-muted font-medium uppercase tracking-wider">
          Intelligence Modules
        </div>
        <ul className="space-y-1" role="list">
          {navigation.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2.5 rounded-radius-md transition-all duration-fast",
                    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-cyan focus-visible:ring-offset-2 focus-visible:ring-offset-background",
                    isActive
                      ? "bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/30"
                      : "text-text-secondary hover:text-text-PRIMARY hover:bg-surface-elevated",
                    collapsed && "justify-center px-2"
                  )}
                  aria-current={isActive ? "page" : undefined}
                  title={collapsed ? item.name : undefined}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" aria-hidden="true" />
                  {!collapsed && (
                    <>
                      <span className="text-body-sm font-medium truncate">{item.name}</span>
                      {item.badge && (
                        <span
                          className={cn(
                            "ml-auto badge",
                            BADGE_COLORS[item.badgeColor || "info"]
                          )}
                        >
                          {item.badge}
                        </span>
                      )}
                    </>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>

        {!collapsed && (
          <>
            <div className="border-t border-border my-2" />
            <div className="px-3 py-2 text-caption text-text-muted font-medium uppercase tracking-wider">
              System
            </div>
            <ul className="space-y-1" role="list">
              {[
                { name: "Memory Pipeline", href: "/settings/memory", icon: Brain },
                { name: "Integrations", href: "/settings/integrations", icon: Zap },
                { name: "Security", href: "/settings/security", icon: Shield },
                { name: "Analytics", href: "/settings/analytics", icon: BarChart3 },
              ].map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="flex items-center gap-3 px-3 py-2.5 rounded-radius-md text-text-secondary hover:text-text-PRIMARY hover:bg-surface-elevated transition-all duration-fast focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-cyan focus-visible:ring-offset-2 focus-visible:ring-offset-background"
                  >
                    <item.icon className="w-5 h-5 flex-shrink-0" aria-hidden="true" />
                    <span className="text-body-sm font-medium truncate">{item.name}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </>
        )}
      </nav>

      {/* Footer / User section */}
      <div className="p-4 border-t border-border">
        {!collapsed ? (
          <div className="space-y-2">
            <Link
              href="/settings"
              className="flex items-center gap-3 px-3 py-2.5 rounded-radius-md text-text-secondary hover:text-text-PRIMARY hover:bg-surface-elevated transition-all duration-fast"
            >
              <Settings className="w-5 h-5 flex-shrink-0" aria-hidden="true" />
              <span className="text-body-sm font-medium">Settings</span>
            </Link>
            <Link
              href="/docs"
              className="flex items-center gap-3 px-3 py-2.5 rounded-radius-md text-text-secondary hover:text-text-PRIMARY hover:bg-surface-elevated transition-all duration-fast"
            >
              <HelpCircle className="w-5 h-5 flex-shrink-0" aria-hidden="true" />
              <span className="text-body-sm font-medium">Documentation</span>
            </Link>
          </div>
        ) : (
          <div className="flex justify-center space-y-2">
            <Link
              href="/settings"
              className="btn-ghost p-2"
              title="Settings"
            >
              <Settings className="w-5 h-5" />
            </Link>
            <Link
              href="/docs"
              className="btn-ghost p-2"
              title="Documentation"
            >
              <HelpCircle className="w-5 h-5" />
            </Link>
          </div>
        )}
      </div>

      {/* Mobile overlay */}
      {isMobile && open && (
        <div
          className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => onToggle(false)}
          aria-hidden="true"
        />
      )}
    </aside>
  );
}
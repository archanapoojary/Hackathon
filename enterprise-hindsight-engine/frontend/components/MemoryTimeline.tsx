"use client";

import React from "react";
import { Clock, MessageSquare, AlertCircle, CheckCircle2, ShieldAlert } from "lucide-react";

export interface MemoryEvent {
  id: string;
  timestamp: string;
  type: "interaction" | "objection" | "resolution" | "milestone";
  title: string;
  content: string;
  author: string;
  tags?: string[];
}

interface MemoryTimelineProps {
  events: MemoryEvent[];
}

export function MemoryTimeline({ events }: MemoryTimelineProps) {
  const getIcon = (type: MemoryEvent["type"]) => {
    switch (type) {
      case "objection":
        return <AlertCircle className="w-4 h-4 text-amber-400" />;
      case "resolution":
        return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      case "milestone":
        return <ShieldAlert className="w-4 h-4 text-cyan-400" />;
      default:
        return <MessageSquare className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="relative border-l border-slate-800 ml-4 space-y-6">
      {events.map((event) => (
        <div key={event.id} className="relative pl-6">
          <div className="absolute -left-3 top-0.5 p-1 rounded-full bg-slate-900 border border-slate-800">
            {getIcon(event.type)}
          </div>
          <div className="bg-slate-900/60 border border-slate-800/80 rounded-lg p-4">
            <div className="flex items-center justify-between gap-2 mb-1">
              <h4 className="text-sm font-semibold text-slate-200">{event.title}</h4>
              <span className="text-xs text-slate-500 font-mono flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {event.timestamp}
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed mb-3">{event.content}</p>
            <div className="flex items-center justify-between text-xs text-slate-500">
              <span>By {event.author}</span>
              {event.tags && (
                <div className="flex gap-1">
                  {event.tags.map((tag, idx) => (
                    <span key={idx} className="px-1.5 py-0.5 bg-slate-800 rounded text-slate-400">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
export default MemoryTimeline;
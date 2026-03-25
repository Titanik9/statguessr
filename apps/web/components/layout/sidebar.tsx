import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { navItems } from "@/lib/navigation";

export function Sidebar() {
  return (
    <aside className="flex h-full flex-col rounded-shell border border-line bg-paper/85 p-5 shadow-soft">
      <div className="mb-8">
        <div className="text-xs uppercase tracking-[0.2em] text-muted">Relay Console</div>
        <div className="mt-2 text-2xl font-semibold tracking-tight text-ink">Control plane</div>
        <p className="mt-3 text-sm leading-6 text-muted">
          Build, release, inspect, and score prompts and agent runs from one self-hosted console.
        </p>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="flex items-center justify-between rounded-2xl px-4 py-3 text-sm text-ink transition hover:bg-white"
          >
            <span>{item.label}</span>
            <Badge tone={item.status === "live" ? "live" : "next"}>{item.status}</Badge>
          </Link>
        ))}
      </nav>

      <div className="mt-auto rounded-3xl border border-dashed border-line bg-canvas px-4 py-5">
        <div className="text-xs uppercase tracking-[0.18em] text-muted">Current sprint</div>
        <div className="mt-2 text-base font-semibold text-ink">Tenancy baseline</div>
        <p className="mt-2 text-sm leading-6 text-muted">
          Magic links, memberships, RBAC, and API keys are wired first so later runtime features inherit the right guardrails.
        </p>
      </div>
    </aside>
  );
}

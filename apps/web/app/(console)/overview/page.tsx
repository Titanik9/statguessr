import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { milestoneRows, overviewStats, promptPreview, requestPreview } from "@/lib/demo-data";

export default function OverviewPage() {
  return (
    <div className="space-y-8">
      <div>
        <div className="text-xs uppercase tracking-[0.18em] text-muted">Overview</div>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-ink">Original control plane for prompts, runtime, and agents</h1>
        <p className="mt-4 max-w-4xl text-sm leading-7 text-muted">
          The repository now has the architectural backbone for the full product: docs, schema, API surface, tenancy, magic links, RBAC, API keys, and audit logs.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {overviewStats.map((stat) => (
          <Card key={stat.label}>
            <div className="text-xs uppercase tracking-[0.16em] text-muted">{stat.label}</div>
            <div className="mt-4 text-4xl font-semibold tracking-tight text-ink">{stat.value}</div>
            <p className="mt-3 text-sm leading-6 text-muted">{stat.note}</p>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs uppercase tracking-[0.18em] text-muted">Delivery plan</div>
              <h2 className="mt-2 text-2xl font-semibold text-ink">Phase checkpoints</h2>
            </div>
            <Badge tone="live">active</Badge>
          </div>
          <div className="mt-6 space-y-4">
            {milestoneRows.map((row) => (
              <div key={row.phase} className="grid gap-3 rounded-3xl border border-line bg-white/80 px-5 py-4 md:grid-cols-[120px_minmax(0,1fr)_120px]">
                <div className="text-sm font-semibold text-ink">{row.phase}</div>
                <div className="text-sm text-muted">{row.scope}</div>
                <div className="text-sm uppercase tracking-[0.14em] text-emerald">{row.status}</div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="text-xs uppercase tracking-[0.18em] text-muted">Upcoming seeded assets</div>
          <h2 className="mt-2 text-2xl font-semibold text-ink">Prompt catalog preview</h2>
          <div className="mt-6 space-y-4">
            {promptPreview.map((row) => (
              <div key={row.name} className="rounded-3xl border border-line bg-white/80 px-5 py-4">
                <div className="flex items-center justify-between">
                  <div className="text-base font-semibold text-ink">{row.name}</div>
                  <Badge tone="next">{row.version}</Badge>
                </div>
                <div className="mt-2 text-sm text-muted">{row.release}</div>
                <div className="mt-1 text-sm text-muted">{row.note}</div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs uppercase tracking-[0.18em] text-muted">Request ledger</div>
            <h2 className="mt-2 text-2xl font-semibold text-ink">Reserved runtime lanes</h2>
          </div>
          <Badge tone="next">phase 4</Badge>
        </div>
        <div className="mt-6 grid gap-4">
          {requestPreview.map((request) => (
            <div key={request.id} className="grid gap-3 rounded-3xl border border-line bg-white/80 px-5 py-4 md:grid-cols-4">
              <div className="font-mono text-sm text-ink">{request.id}</div>
              <div className="text-sm text-muted">{request.prompt}</div>
              <div className="text-sm text-muted">{request.status}</div>
              <div className="text-sm text-muted">{request.score}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-xs uppercase tracking-[0.18em] text-muted">Settings</div>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-ink">Identity, tenancy, and access controls</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-muted">
          This first working slice is centered here. The API already has endpoints for magic links, workspace creation, membership updates, API key creation, and audit logs.
        </p>
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs uppercase tracking-[0.18em] text-muted">RBAC</div>
              <h2 className="mt-2 text-2xl font-semibold text-ink">Workspace roles</h2>
            </div>
            <Badge tone="live">phase 2</Badge>
          </div>
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {[
              ["owner", "Full control, including role elevation and destructive actions."],
              ["admin", "Workspace administration, members, API keys, and audit review."],
              ["editor", "Safe prompt and runtime editing once registry features land."],
              ["viewer", "Read-only access for operators and reviewers."],
            ].map(([role, description]) => (
              <div key={role} className="rounded-3xl border border-line bg-white/80 px-5 py-4">
                <div className="text-base font-semibold text-ink">{role}</div>
                <div className="mt-2 text-sm leading-6 text-muted">{description}</div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="text-xs uppercase tracking-[0.18em] text-muted">API keys</div>
          <h2 className="mt-2 text-2xl font-semibold text-ink">Lifecycle rules</h2>
          <ul className="mt-5 space-y-3 text-sm leading-6 text-muted">
            <li>Keys are shown once and stored hashed with a short prefix for display.</li>
            <li>Creation and revocation both emit audit events with request IDs.</li>
            <li>Admin-level membership is required for management endpoints.</li>
          </ul>
        </Card>
      </div>

      <Card>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs uppercase tracking-[0.18em] text-muted">Audit trail</div>
            <h2 className="mt-2 text-2xl font-semibold text-ink">Mutation capture</h2>
          </div>
          <Badge tone="live">available</Badge>
        </div>
        <div className="mt-6 grid gap-4">
          {[
            { action: "workspace.create", note: "Recorded when a workspace is created." },
            { action: "workspace.member.update", note: "Recorded when a role changes." },
            { action: "api_key.create", note: "Recorded when a workspace key is issued." },
            { action: "api_key.revoke", note: "Recorded when a key is revoked." },
          ].map((row) => (
            <div key={row.action} className="grid gap-3 rounded-3xl border border-line bg-white/80 px-5 py-4 md:grid-cols-[220px_minmax(0,1fr)]">
              <div className="font-mono text-sm text-ink">{row.action}</div>
              <div className="text-sm text-muted">{row.note}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

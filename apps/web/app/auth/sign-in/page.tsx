import { Card } from "@/components/ui/card";
import { MagicLinkForm } from "@/components/auth/magic-link-form";

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-10">
      <div className="grid w-full max-w-5xl gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <Card className="relative overflow-hidden bg-paper p-8 lg:p-10">
          <div className="text-xs uppercase tracking-[0.18em] text-muted">Relay Console</div>
          <h1 className="mt-4 max-w-lg text-4xl font-semibold tracking-tight text-ink">
            Release prompts and inspect agent behavior with a control plane built for teams.
          </h1>
          <p className="mt-4 max-w-xl text-base leading-7 text-muted">
            This first slice focuses on sign-in, workspace management, roles, and API keys so the rest of the platform has a secure backbone from day one.
          </p>
          <div className="mt-8 grid gap-4 md:grid-cols-2">
            <div className="rounded-3xl border border-line bg-white/70 p-5">
              <div className="text-sm font-semibold text-ink">Phase 2 in motion</div>
              <p className="mt-2 text-sm leading-6 text-muted">
                Magic links, tenancy boundaries, and audit trails are being wired before runtime logging and registry features land.
              </p>
            </div>
            <div className="rounded-3xl border border-line bg-white/70 p-5">
              <div className="text-sm font-semibold text-ink">Self-host first</div>
              <p className="mt-2 text-sm leading-6 text-muted">
                PostgreSQL, ClickHouse, Redis, MinIO, and Mailpit are part of the local stack so teams can own deployment and data residency.
              </p>
            </div>
          </div>
        </Card>
        <Card className="bg-white/95 p-8">
          <div className="text-xs uppercase tracking-[0.18em] text-muted">Sign in</div>
          <h2 className="mt-3 text-2xl font-semibold text-ink">Email a one-time link</h2>
          <p className="mt-3 text-sm leading-6 text-muted">
            In development mode, the API returns a preview URL directly so the flow can be exercised without a real SMTP provider.
          </p>
          <div className="mt-8">
            <MagicLinkForm />
          </div>
        </Card>
      </div>
    </div>
  );
}

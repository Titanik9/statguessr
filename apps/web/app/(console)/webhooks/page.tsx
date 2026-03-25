import { SectionPage } from "@/components/layout/section-page";

export default function WebhooksPage() {
  return (
    <SectionPage
      eyebrow="Webhooks"
      title="Signed outbound sync hooks"
      description="Webhook configuration and delivery history will live here once the event system is wired in."
      rows={[
        { lane: "Destinations", capability: "Workspace-managed callbacks", status: "queued", phase: "9 / 12" },
        { lane: "Signing", capability: "Per-endpoint signature secrets", status: "queued", phase: "12" },
        { lane: "Retries", capability: "Worker-driven delivery attempts", status: "queued", phase: "12" },
      ]}
    />
  );
}

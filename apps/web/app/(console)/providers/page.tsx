import { SectionPage } from "@/components/layout/section-page";

export default function ProvidersPage() {
  return (
    <SectionPage
      eyebrow="Providers"
      title="Provider and model catalog"
      description="Built-in and custom adapters will live here, including workspace credentials, health checks, and model availability."
      rows={[
        { lane: "Adapters", capability: "OpenAI-compatible plus custom bridges", status: "queued", phase: "9" },
        { lane: "Credentials", capability: "Encrypted per-workspace provider secrets", status: "queued", phase: "9" },
        { lane: "Health", capability: "Connectivity checks and catalog refresh", status: "queued", phase: "9" },
      ]}
    />
  );
}

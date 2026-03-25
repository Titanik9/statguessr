import { SectionPage } from "@/components/layout/section-page";

export default function RequestsPage() {
  return (
    <SectionPage
      eyebrow="Requests"
      title="Unified runtime ledger"
      description="This screen is reserved for searchable request logs with prompt snapshots, model/provider details, metadata, scores, and links into trace detail."
      rows={[
        { lane: "Run API", capability: "Request IDs and prompt resolution", status: "queued", phase: "4" },
        { lane: "Search", capability: "Tags, metadata, scores, and actor filters", status: "queued", phase: "4" },
        { lane: "Detail view", capability: "Snapshot, output, trace link, feedback", status: "queued", phase: "4" },
      ]}
    />
  );
}

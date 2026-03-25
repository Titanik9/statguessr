import { SectionPage } from "@/components/layout/section-page";

export default function TracesPage() {
  return (
    <SectionPage
      eyebrow="Traces"
      title="Root traces and span trees"
      description="This reserved area will visualize agent, LLM, tool, function, retriever, and webhook spans with inputs, outputs, timings, and failures."
      rows={[
        { lane: "Ingestion", capability: "OpenTelemetry-compatible path", status: "queued", phase: "5" },
        { lane: "Viewer", capability: "Tree navigation and detail panel", status: "queued", phase: "5" },
        { lane: "Linking", capability: "Cross-links to requests and agent runs", status: "queued", phase: "5 / 10" },
      ]}
    />
  );
}

import { SectionPage } from "@/components/layout/section-page";

export default function AgentsPage() {
  return (
    <SectionPage
      eyebrow="Agents"
      title="Versioned workflow graphs"
      description="Agents will be modeled as small DAGs with prompt calls, code steps, conditions, and tools, with replay and trace-aware debugging."
      rows={[
        { lane: "Definitions", capability: "Versioned DAG schemas", status: "queued", phase: "10" },
        { lane: "Runs", capability: "Inputs, outputs, replay, and traces", status: "queued", phase: "10" },
        { lane: "Tooling", capability: "Prompt, function, condition, and tool nodes", status: "queued", phase: "10" },
      ]}
    />
  );
}

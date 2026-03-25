import { SectionPage } from "@/components/layout/section-page";

export default function PromptsPage() {
  return (
    <SectionPage
      eyebrow="Prompts"
      title="Registry, versions, and releases"
      description="This view is scaffolded for the next phase. It will hold prompt templates, immutable versions, diffs, release labels, linting feedback, and usage context."
      rows={[
        { lane: "Registry", capability: "Template variables and change messages", status: "queued", phase: "3" },
        { lane: "Release labels", capability: "dev, staging, prod plus A/B variants", status: "queued", phase: "3 / 8" },
        { lane: "Linting", capability: "Missing variables, token estimate, secrets scan", status: "queued", phase: "3" },
      ]}
    />
  );
}

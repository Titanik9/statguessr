import { SectionPage } from "@/components/layout/section-page";

export default function EvalsPage() {
  return (
    <SectionPage
      eyebrow="Evals"
      title="Reusable evaluators and regression runs"
      description="The evaluation system will compare prompt and agent versions across datasets with rule-based checks, semantic checks, LLM judges, and human scores."
      rows={[
        { lane: "Evaluators", capability: "Exact match, regex, schema, semantic, judge", status: "queued", phase: "7" },
        { lane: "Pipelines", capability: "Reusable ordered steps", status: "queued", phase: "7" },
        { lane: "Comparison", capability: "Baseline versus candidate drift analysis", status: "queued", phase: "7 / 8" },
      ]}
    />
  );
}

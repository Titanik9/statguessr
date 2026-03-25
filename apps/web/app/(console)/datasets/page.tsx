import { SectionPage } from "@/components/layout/section-page";

export default function DatasetsPage() {
  return (
    <SectionPage
      eyebrow="Datasets"
      title="Rows built from logs or files"
      description="Datasets will be versioned, searchable, and easy to browse so evaluation runs have a stable source of truth."
      rows={[
        { lane: "From logs", capability: "Convert selected requests into examples", status: "queued", phase: "6" },
        { lane: "Uploads", capability: "CSV and JSON import into MinIO-backed objects", status: "queued", phase: "6" },
        { lane: "Versioning", capability: "Stable snapshots and row schemas", status: "queued", phase: "6" },
      ]}
    />
  );
}

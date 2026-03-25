export const overviewStats = [
  { label: "Active workspaces", value: "3", note: "Identity and RBAC foundation ready" },
  { label: "Tracked request lanes", value: "12", note: "Reserved for run, trace, and eval surfaces" },
  { label: "Provider adapters", value: "4", note: "OpenAI-compatible, Anthropic-style, Gemini-style, custom" },
  { label: "Phase progress", value: "2 / 12", note: "Docs and tenancy are in place" },
];

export const milestoneRows = [
  { phase: "Phase 1", scope: "Docs, schema, OpenAPI", status: "done" },
  { phase: "Phase 2", scope: "Auth, workspaces, RBAC, API keys", status: "in progress" },
  { phase: "Phase 3", scope: "Prompt registry and releases", status: "queued" },
  { phase: "Phase 4", scope: "Runs and request logging", status: "queued" },
];

export const requestPreview = [
  { id: "req_4d8f", prompt: "support-bot", status: "queued", latency: "n/a", score: "pending" },
  { id: "req_a93c", prompt: "summary", status: "queued", latency: "n/a", score: "pending" },
];

export const promptPreview = [
  { name: "support-bot", version: "v2", release: "prod 50%", note: "A/B ready" },
  { name: "summary", version: "v1", release: "staging", note: "Seed prompt planned" },
];

# Relay Console PRD

## Product summary

Relay Console is a self-hosted control plane for prompt development, runtime logging, evaluations, release management, and lightweight agent orchestration. It targets teams that want production discipline around LLM prompts and agents without depending on a hosted third-party control plane.

## Primary users

- Platform engineer managing providers, environments, and deployment controls
- Application engineer iterating on prompts, agents, and regression tests
- ML or QA analyst reviewing runs, datasets, traces, and evaluator results
- Workspace admin handling access, API keys, and auditability

## Core outcomes

1. Teams can version prompts and promote them safely across environments.
2. Every execution yields a stable `request_id` and traceable runtime record.
3. Regression checks catch quality, cost, or latency drift before rollout.
4. Custom providers and agent workflows plug into a consistent interface.
5. Self-hosted operators can deploy and extend the platform without SaaS lock-in.

## Category capabilities

- Prompt registry with template variables, versions, labels, diffs, and rollback
- Prompt playground and unified run API
- Logging with metadata, tags, feedback, scores, and request search
- Agent and LLM tracing with root traces and spans
- Datasets created from logs or uploaded files
- Evaluation pipelines with reusable evaluators and regression comparison
- A/B routing through release labels with weighted traffic and sticky assignment
- Provider and model catalog management
- Webhooks, audit logs, RBAC, API keys, and workspace isolation
- Analytics dashboards for usage, spend, quality, and operations

## MVP scope

### Phase 1

- PRD, architecture, schema, migration plan, OpenAPI contract, deployment notes

### Phase 2

- Email magic link auth
- Workspaces and memberships
- Roles: `owner`, `admin`, `editor`, `viewer`
- API key lifecycle
- Audit logs for mutations
- Console shell with navigation and core settings surfaces

### Phase 3

- Prompt templates and versions
- Release labels
- Diff, rollback, and linting

### Phase 4

- Run API
- Request logging and request detail UI
- Metadata, tags, feedback, and score capture

### Phase 5

- Trace ingestion
- Span storage
- Tree viewer

### Phase 6

- Datasets from logs
- File upload
- Dataset versioning and row browser

### Phase 7

- Evaluators
- Pipelines
- Batch eval runs
- Regression comparison

### Phase 8

- Weighted prompt releases
- Sticky assignment
- Variant analytics

### Phase 9

- Provider adapters
- Workspace credentials
- Model catalog and health checks

### Phase 10

- Versioned agent DAGs
- Agent runs and replay

### Phase 11

- Analytics dashboards

### Phase 12

- Security hardening
- Broader test coverage
- Operational docs

## Non-goals for MVP

- Fine-grained billing or invoicing
- Marketplace/distribution features
- End-user chat UI
- Autonomous agent scheduling beyond manual or API-triggered runs
- Deep Kubernetes operator automation in the first cut

## Functional requirements

### Prompt registry

- Create prompt templates with structured variables
- Store immutable versions with change messages
- Diff versions and rollback to prior text/config
- Assign and resolve release labels
- Enforce variable validation and linting

### Runtime

- Single run API returns `request_id`
- Runtime logs include actor, prompt snapshot, provider/model, params, timing, tokens, cost, tags, metadata, and outputs
- SDK hooks can log external provider executions without routing traffic through Relay Console

### Tracing

- Root traces with nested spans
- Span types for `agent`, `llm`, `tool`, `retriever`, `function`, `webhook`
- Inputs, outputs, timings, metadata, and errors stored per span

### Data and evaluation

- Datasets built from logs or file uploads
- Versioned datasets with stable row identifiers
- Evaluators for rule-based, semantic, LLM-judge, human, and custom code checks
- Batch eval runs and comparisons between prompt or agent versions

### Security and operations

- Tenant isolation at the workspace boundary
- Email magic link auth plus API keys
- Secret encryption at rest
- Signed webhooks with retries
- Audit logs for all mutating actions
- Rate limiting and idempotency on critical endpoints

## Success criteria

- `docker compose up` boots web, API, worker, PostgreSQL, Redis, ClickHouse, MinIO, and Mailpit
- A user can sign in, create a workspace, create an API key, and view audit events
- A user can later create prompts, run them, inspect logs, create datasets, and execute evals without schema redesign

## Assumptions

- PostgreSQL is the system of record; ClickHouse is optimized for analytics and time-series queries
- OpenTelemetry-compatible trace ingestion is required but can be stored in the platform schema for the MVP
- Local development values fast feedback over perfect production parity, while deployment artifacts remain production-oriented

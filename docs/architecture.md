# Architecture

## High-level decisions

### 1. Monorepo with split runtime stacks

- `apps/web` holds the Next.js 15 console
- `apps/api` holds FastAPI, background job entrypoints, and migrations
- `packages/ts-sdk` and `packages/py-sdk` expose client libraries

Rationale:

- Frontend and backend evolve together around a shared product contract
- Python remains the best fit for evaluator logic, prompt linting, and batch orchestration
- TypeScript remains the best fit for the admin UI and browser-friendly SDK

### 2. FastAPI over NestJS

Rationale:

- Faster delivery for an API-heavy MVP
- Pydantic models become the source of truth for validation and OpenAPI
- Celery is a practical path for evaluation runs, webhook retries, and file ingestion
- Future provider adapters, evaluators, and data tooling naturally live in Python

### 3. Dual data stores

- PostgreSQL stores normalized product state
- ClickHouse stores high-volume runtime analytics
- Redis supports task queueing, rate limit counters, cache, and sticky A/B assignment
- MinIO stores file uploads, dataset artifacts, and export bundles

Rationale:

- Product workflows need relational integrity
- Analytics and trace exploration need inexpensive aggregation over large event volumes

### 4. Original console UX

- Left navigation with domain-oriented views
- Emphasis on run detail, prompt lineage, trace trees, and score comparison
- Warm neutral palette with emerald accents instead of the common dark-purple SaaS pattern

## Runtime topology

```text
Browser
  -> Next.js console
    -> FastAPI REST API
      -> PostgreSQL
      -> Redis
      -> MinIO
      -> ClickHouse
      -> Celery worker
      -> Provider adapters / webhook destinations
```

## Backend module boundaries

```text
relay_console/
├── api             # Router composition and request dependencies
├── core            # Config, logging, security, encryption, telemetry
├── db              # Engine, session factory, ORM base
└── modules
    ├── auth        # Magic links, sessions, identity
    ├── iam         # Workspaces, memberships, RBAC
    ├── api_keys    # Key issuance and revocation
    ├── audit       # Audit events
    ├── prompts     # Future prompt registry
    ├── runtime     # Future run logging
    ├── traces      # Future trace ingestion and viewer support
    ├── datasets    # Future datasets and uploads
    ├── evals       # Future evaluators and pipelines
    ├── agents      # Future workflows and agent runs
    └── providers   # Future provider catalog and credentials
```

Each module owns:

- ORM models
- Pydantic request/response schemas
- service functions
- router definitions

This keeps business logic close to its schema and transport boundary while avoiding a single monolithic `models.py` or `routers.py`.

## Frontend structure

```text
apps/web
├── app
│   ├── auth
│   └── (console)
├── components
│   ├── layout
│   └── ui
└── lib
```

Patterns:

- App Router with server components by default
- Small client components only for forms and interactive panels
- Utility-first styling with a light, editorial admin aesthetic
- Shared `ui` components so later domain screens stay visually consistent without cloning another product

## Security model

- Workspace-scoped access checks on every protected route
- Session tokens signed and stored with server-side revocation support
- API keys stored as hashes with prefix display only
- Secrets encrypted before persistence using an operator-provided key
- Audit log entries emitted for create/update/delete flows
- Idempotency keys required for externally retried write APIs
- PII redaction hooks inserted before long-term log persistence

## Observability

- Structured application logs from API and worker
- OpenTelemetry tracing emitted by API and worker
- Request IDs propagated through API, worker jobs, traces, webhook deliveries, and provider adapters

## Folder structure target

```text
.
├── apps
│   ├── api
│   │   ├── alembic
│   │   ├── src/relay_console
│   │   └── tests
│   └── web
│       ├── app
│       ├── components
│       └── lib
├── docs
├── infra
│   └── compose
├── packages
│   ├── py-sdk
│   └── ts-sdk
└── legacy
    └── statguessr
```

## Near-term implementation plan

1. Identity, workspaces, RBAC, API keys, audit trail
2. Prompt registry and release resolution
3. Run logging and request detail screens
4. Traces, datasets, and eval pipelines
5. Providers, agents, analytics, and hardening

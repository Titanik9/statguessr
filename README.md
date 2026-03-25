# Relay Console

Relay Console is an original, self-hosted AI prompt and agent management platform for teams that need prompt versioning, runtime observability, evaluations, release controls, and multi-provider execution.

This repository is now organized as a product monorepo. The previous static StatGuessr prototype was preserved under [`legacy/statguessr/`](/Users/yehornekrasov/Documents/New%20project/legacy/statguessr/README.md) so the new platform can evolve without losing the old work.

## Current status

- Product docs and API surface drafted
- Monorepo scaffold created
- Phase 2 foundation in progress: auth, workspaces, RBAC, API keys

## Why FastAPI

The backend uses FastAPI instead of NestJS because it gets us to a working platform faster for this domain:

- Pydantic gives strong request validation and OpenAPI generation
- Celery integrates naturally for async evals and webhook delivery
- Python is a better home for evaluator plugins, prompt linting, and data tooling
- The Python SDK can dogfood the same models and runtime conventions

## Monorepo layout

```text
.
├── apps
│   ├── api                  # FastAPI app, Alembic migrations, Celery entrypoints
│   └── web                  # Next.js 15 admin console
├── docs                     # PRD, architecture, schema, API surface, deployment notes
├── infra
│   └── compose              # Docker Compose stack and local infrastructure config
├── legacy
│   └── statguessr           # Preserved previous static prototype
├── packages
│   ├── py-sdk               # Python SDK scaffold
│   └── ts-sdk               # TypeScript SDK scaffold
├── Makefile
└── package.json
```

## First milestones

1. Identity, workspaces, RBAC, and API keys
2. Prompt registry and release labels
3. Run API, request logs, and request detail pages
4. Traces, datasets, evals, and analytics

## Local development

The repository is scaffolded for `npm` workspaces and Python `venv` usage in this environment. Docker Compose files are included for the intended self-hosted deployment path, but Docker is not installed in the current shell session so the stack has not been started here yet.

See:

- [`docs/prd.md`](/Users/yehornekrasov/Documents/New%20project/docs/prd.md)
- [`docs/architecture.md`](/Users/yehornekrasov/Documents/New%20project/docs/architecture.md)
- [`docs/schema.md`](/Users/yehornekrasov/Documents/New%20project/docs/schema.md)
- [`docs/openapi.yaml`](/Users/yehornekrasov/Documents/New%20project/docs/openapi.yaml)
- [`docs/deployment.md`](/Users/yehornekrasov/Documents/New%20project/docs/deployment.md)

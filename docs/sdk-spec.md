# SDK Specification

## Goals

- Provide thin, typed clients for the Relay Console REST API
- Support both routed execution and bring-your-own provider logging hooks
- Keep SDKs stable even while the web console evolves

## TypeScript SDK

Location:

- `packages/ts-sdk`

Design:

- ESM-first package with fetch-based transport
- `RelayClient` configured with `baseUrl`, `apiKey`, or `sessionToken`
- Strong request/response types aligned with `docs/openapi.yaml`

Primary methods:

- `auth.requestMagicLink()`
- `auth.verifyMagicLink()`
- `workspaces.list()`
- `workspaces.create()`
- `apiKeys.list()`
- `apiKeys.create()`
- `prompts.run()`
- `requests.list()`
- `traces.ingest()`
- `datasets.createFromLogs()`
- `evals.run()`
- `agents.run()`

## Python SDK

Location:

- `packages/py-sdk`

Design:

- `httpx`-based sync client for the MVP
- Pydantic-friendly dictionaries and dataclasses where useful
- Simple hook API for logging external LLM calls into Relay Console

Primary methods:

- `request_magic_link`
- `verify_magic_link`
- `list_workspaces`
- `create_workspace`
- `create_api_key`
- `run_prompt`
- `log_trace`
- `create_dataset_from_logs`

## Auth modes

- Session bearer token from magic link verification
- Workspace-scoped API key via header

## Stability plan

- `/v1` versioned API namespace
- Additive fields preferred over breaking response reshapes
- SDK wrappers keep transport concerns centralized so retries, idempotency, and tracing headers can evolve without broad call-site changes

# Database Schema

## Design notes

- PostgreSQL is the transactional source of truth.
- ClickHouse stores append-heavy analytics events and derived aggregates.
- Flexible metadata stays in `JSONB` where strict normalization would hurt usability or ingestion speed.
- Business entities and relationships stay normalized with explicit foreign keys and unique constraints.

## PostgreSQL tables

### Identity and tenancy

#### `users`

- `id` `varchar(36)` primary key
- `email` `citext` unique not null
- `display_name` `varchar(120)` null
- `status` `varchar(32)` not null
- `last_login_at` `timestamptz` null
- `created_at` `timestamptz` not null
- `updated_at` `timestamptz` not null
- `deleted_at` `timestamptz` null

Indexes:

- unique `users_email_key`
- btree on `status`

#### `magic_link_tokens`

- `id` primary key
- `user_id` fk -> `users.id`
- `workspace_id` fk -> `workspaces.id` null
- `token_hash` unique not null
- `purpose` `varchar(32)` not null
- `expires_at` `timestamptz` not null
- `consumed_at` `timestamptz` null
- `requested_ip` `varchar(64)` null
- `created_at` `timestamptz` not null

Indexes:

- unique `token_hash`
- btree on `user_id, expires_at`

#### `auth_sessions`

- `id` primary key
- `user_id` fk -> `users.id`
- `workspace_id` fk -> `workspaces.id` null
- `session_hash` unique not null
- `user_agent` `varchar(255)` null
- `ip_address` `varchar(64)` null
- `expires_at` `timestamptz` not null
- `revoked_at` `timestamptz` null
- `last_seen_at` `timestamptz` null
- `created_at` `timestamptz` not null

Indexes:

- unique `session_hash`
- btree on `user_id, revoked_at`

#### `workspaces`

- `id` primary key
- `slug` unique not null
- `name` `varchar(120)` not null
- `plan_tier` `varchar(32)` not null
- `default_region` `varchar(32)` not null
- `created_by_user_id` fk -> `users.id`
- `created_at` `timestamptz` not null
- `updated_at` `timestamptz` not null
- `deleted_at` `timestamptz` null

Indexes:

- unique `slug`
- btree on `created_by_user_id`

#### `workspace_memberships`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `user_id` fk -> `users.id`
- `role` `varchar(16)` not null
- `invited_by_user_id` fk -> `users.id` null
- `joined_at` `timestamptz` null
- `accepted_at` `timestamptz` null
- `created_at` `timestamptz` not null
- `updated_at` `timestamptz` not null

Constraints:

- unique `(workspace_id, user_id)`

Indexes:

- btree on `workspace_id, role`
- btree on `user_id`

#### `api_keys`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `created_by_user_id` fk -> `users.id`
- `label` `varchar(120)` not null
- `key_prefix` `varchar(16)` not null
- `key_hash` unique not null
- `scopes_json` `jsonb` not null
- `last_used_at` `timestamptz` null
- `expires_at` `timestamptz` null
- `revoked_at` `timestamptz` null
- `created_at` `timestamptz` not null

Indexes:

- unique `key_hash`
- btree on `workspace_id, revoked_at`

#### `audit_logs`

- `id` primary key
- `workspace_id` fk -> `workspaces.id` null
- `actor_user_id` fk -> `users.id` null
- `actor_api_key_id` fk -> `api_keys.id` null
- `action` `varchar(64)` not null
- `target_type` `varchar(64)` not null
- `target_id` `varchar(36)` not null
- `request_id` `varchar(64)` null
- `before_json` `jsonb` null
- `after_json` `jsonb` null
- `created_at` `timestamptz` not null

Indexes:

- btree on `workspace_id, created_at desc`
- btree on `target_type, target_id`

### Provider and model catalog

#### `providers`

- `id` primary key
- `workspace_id` fk -> `workspaces.id` null
- `kind` `varchar(16)` not null
- `slug` `varchar(64)` not null
- `display_name` `varchar(120)` not null
- `adapter` `varchar(64)` not null
- `base_url` `text` null
- `auth_strategy` `varchar(32)` not null
- `status` `varchar(16)` not null
- `created_at`, `updated_at`

Constraints:

- unique `(workspace_id, slug)`

#### `workspace_secrets`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `provider_id` fk -> `providers.id`
- `secret_name` `varchar(64)` not null
- `encrypted_value` `text` not null
- `key_version` `varchar(32)` not null
- `created_by_user_id` fk -> `users.id`
- `created_at`, `updated_at`, `deleted_at`

#### `models`

- `id` primary key
- `provider_id` fk -> `providers.id`
- `workspace_id` fk -> `workspaces.id` null
- `identifier` `varchar(128)` not null
- `display_name` `varchar(120)` not null
- `family` `varchar(64)` not null
- `capabilities_json` `jsonb` not null
- `pricing_json` `jsonb` not null
- `status` `varchar(16)` not null
- `created_at`, `updated_at`

Constraints:

- unique `(provider_id, workspace_id, identifier)`

### Prompt registry

#### `prompt_templates`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `name` `varchar(120)` not null
- `slug` `varchar(120)` not null
- `description` `text` null
- `template_format` `varchar(32)` not null
- `owner_user_id` fk -> `users.id`
- `created_at`, `updated_at`, `archived_at`

Constraints:

- unique `(workspace_id, slug)`
- unique `(workspace_id, name)`

#### `prompt_versions`

- `id` primary key
- `prompt_template_id` fk -> `prompt_templates.id`
- `version_number` `integer` not null
- `change_message` `varchar(255)` null
- `template_text` `text` not null
- `variables_schema_json` `jsonb` not null
- `default_params_json` `jsonb` not null
- `lint_summary_json` `jsonb` not null
- `token_estimate` `integer` not null
- `created_by_user_id` fk -> `users.id`
- `created_at` not null

Constraints:

- unique `(prompt_template_id, version_number)`

#### `prompt_release_labels`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `name` `varchar(64)` not null
- `description` `text` null
- `created_at`, `updated_at`

Constraints:

- unique `(workspace_id, name)`

#### `prompt_release_variants`

- `id` primary key
- `release_label_id` fk -> `prompt_release_labels.id`
- `prompt_template_id` fk -> `prompt_templates.id`
- `prompt_version_id` fk -> `prompt_versions.id`
- `variant_key` `varchar(64)` not null
- `weight_percent` `numeric(5,2)` not null
- `segment_rule_json` `jsonb` null
- `sticky_key_mode` `varchar(32)` not null
- `is_active` `boolean` not null
- `created_at`, `updated_at`

Indexes:

- btree on `release_label_id, is_active`

### Runtime, requests, and scoring

#### `requests`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `trace_id` fk -> `traces.id` null
- `prompt_template_id` fk -> `prompt_templates.id` null
- `prompt_version_id` fk -> `prompt_versions.id` null
- `release_label_id` fk -> `prompt_release_labels.id` null
- `actor_user_id` fk -> `users.id` null
- `actor_api_key_id` fk -> `api_keys.id` null
- `provider_id` fk -> `providers.id` null
- `model_id` fk -> `models.id` null
- `source` `varchar(32)` not null
- `route_variant` `varchar(64)` null
- `input_variables_json` `jsonb` null
- `rendered_prompt` `text` null
- `request_params_json` `jsonb` not null
- `response_body_json` `jsonb` null
- `output_text` `text` null
- `metadata_json` `jsonb` not null
- `status` `varchar(32)` not null
- `error_code` `varchar(64)` null
- `error_message` `text` null
- `latency_ms` `integer` null
- `input_tokens` `integer` null
- `output_tokens` `integer` null
- `cost_estimate_usd` `numeric(12,6)` null
- `cache_hit` `boolean` not null
- `created_at` `timestamptz` not null

Indexes:

- btree on `workspace_id, created_at desc`
- btree on `prompt_template_id, created_at desc`
- btree on `status, created_at desc`
- gin on `metadata_json`

#### `request_tags`

- `request_id` fk -> `requests.id`
- `tag` `varchar(64)` not null

Constraints:

- primary key `(request_id, tag)`

#### `request_feedback`

- `id` primary key
- `request_id` fk -> `requests.id`
- `author_user_id` fk -> `users.id` null
- `kind` `varchar(32)` not null
- `score_numeric` `numeric(8,3)` null
- `comment` `text` null
- `created_at` `timestamptz` not null

#### `scores`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `request_id` fk -> `requests.id` null
- `eval_run_item_id` fk -> `eval_run_items.id` null
- `evaluator_id` fk -> `evaluators.id` null
- `name` `varchar(64)` not null
- `value_numeric` `numeric(10,4)` null
- `value_label` `varchar(64)` null
- `explanation` `text` null
- `created_at` `timestamptz` not null

### Tracing

#### `traces`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `origin` `varchar(32)` not null
- `status` `varchar(32)` not null
- `root_span_id` `varchar(36)` null
- `metadata_json` `jsonb` not null
- `started_at`, `ended_at`, `duration_ms`, `created_at`

Indexes:

- btree on `workspace_id, started_at desc`

#### `spans`

- `id` primary key
- `trace_id` fk -> `traces.id`
- `parent_span_id` fk -> `spans.id` null
- `request_id` fk -> `requests.id` null
- `agent_run_id` fk -> `agent_runs.id` null
- `span_type` `varchar(32)` not null
- `name` `varchar(120)` not null
- `status` `varchar(32)` not null
- `input_json` `jsonb` null
- `output_json` `jsonb` null
- `error_json` `jsonb` null
- `metadata_json` `jsonb` not null
- `started_at`, `ended_at`, `duration_ms`

Indexes:

- btree on `trace_id, started_at`
- btree on `parent_span_id`

### Datasets and evaluations

#### `datasets`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `name` `varchar(120)` not null
- `description` `text` null
- `source_kind` `varchar(32)` not null
- `created_by_user_id` fk -> `users.id`
- `created_at`, `updated_at`, `archived_at`

#### `dataset_versions`

- `id` primary key
- `dataset_id` fk -> `datasets.id`
- `version_number` `integer` not null
- `source_file_object_id` fk -> `file_objects.id` null
- `source_filter_json` `jsonb` null
- `row_count` `integer` not null
- `schema_json` `jsonb` not null
- `created_by_user_id` fk -> `users.id`
- `created_at` `timestamptz` not null

Constraints:

- unique `(dataset_id, version_number)`

#### `dataset_rows`

- `id` primary key
- `dataset_version_id` fk -> `dataset_versions.id`
- `row_index` `integer` not null
- `input_json` `jsonb` not null
- `expected_output_json` `jsonb` null
- `metadata_json` `jsonb` not null
- `source_request_id` fk -> `requests.id` null
- `source_file_line` `integer` null

Constraints:

- unique `(dataset_version_id, row_index)`

#### `evaluators`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `name` `varchar(120)` not null
- `evaluator_type` `varchar(32)` not null
- `config_json` `jsonb` not null
- `runtime_code_ref` `varchar(255)` null
- `created_by_user_id` fk -> `users.id`
- `created_at`, `updated_at`

#### `eval_pipelines`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `name` `varchar(120)` not null
- `description` `text` null
- `created_by_user_id` fk -> `users.id`
- `created_at`, `updated_at`

#### `eval_pipeline_steps`

- `id` primary key
- `eval_pipeline_id` fk -> `eval_pipelines.id`
- `step_order` `integer` not null
- `step_type` `varchar(32)` not null
- `evaluator_id` fk -> `evaluators.id` null
- `config_json` `jsonb` not null
- `created_at` `timestamptz` not null

Constraints:

- unique `(eval_pipeline_id, step_order)`

#### `eval_runs`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `dataset_version_id` fk -> `dataset_versions.id`
- `eval_pipeline_id` fk -> `eval_pipelines.id`
- `prompt_template_id` fk -> `prompt_templates.id` null
- `baseline_prompt_version_id` fk -> `prompt_versions.id` null
- `candidate_prompt_version_id` fk -> `prompt_versions.id` null
- `agent_version_id` fk -> `agent_versions.id` null
- `status` `varchar(32)` not null
- `summary_json` `jsonb` not null
- `created_by_user_id` fk -> `users.id`
- `started_at`, `completed_at`, `created_at`

#### `eval_run_items`

- `id` primary key
- `eval_run_id` fk -> `eval_runs.id`
- `dataset_row_id` fk -> `dataset_rows.id`
- `request_id` fk -> `requests.id` null
- `status` `varchar(32)` not null
- `output_json` `jsonb` null
- `aggregate_score` `numeric(10,4)` null
- `created_at`, `completed_at`

Constraints:

- unique `(eval_run_id, dataset_row_id)`

#### `eval_item_scores`

- `id` primary key
- `eval_run_item_id` fk -> `eval_run_items.id`
- `evaluator_id` fk -> `evaluators.id`
- `score_numeric` `numeric(10,4)` null
- `passed` `boolean` not null
- `explanation` `text` null
- `raw_json` `jsonb` null
- `created_at` `timestamptz` not null

Constraints:

- unique `(eval_run_item_id, evaluator_id)`

### Agents and integrations

#### `agents`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `name` `varchar(120)` not null
- `description` `text` null
- `created_by_user_id` fk -> `users.id`
- `created_at`, `updated_at`, `archived_at`

#### `agent_versions`

- `id` primary key
- `agent_id` fk -> `agents.id`
- `version_number` `integer` not null
- `change_message` `varchar(255)` null
- `dag_json` `jsonb` not null
- `input_schema_json` `jsonb` not null
- `output_schema_json` `jsonb` not null
- `created_by_user_id` fk -> `users.id`
- `created_at` `timestamptz` not null

Constraints:

- unique `(agent_id, version_number)`

#### `agent_runs`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `agent_id` fk -> `agents.id`
- `agent_version_id` fk -> `agent_versions.id`
- `trace_id` fk -> `traces.id` null
- `created_by_user_id` fk -> `users.id` null
- `api_key_id` fk -> `api_keys.id` null
- `status` `varchar(32)` not null
- `input_json` `jsonb` not null
- `output_json` `jsonb` null
- `error_json` `jsonb` null
- `started_at`, `completed_at`, `created_at`

#### `webhooks`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `name` `varchar(120)` not null
- `target_url` `text` not null
- `signing_secret_encrypted` `text` not null
- `event_types_json` `jsonb` not null
- `status` `varchar(16)` not null
- `created_by_user_id` fk -> `users.id`
- `created_at`, `updated_at`

#### `webhook_deliveries`

- `id` primary key
- `webhook_id` fk -> `webhooks.id`
- `event_type` `varchar(64)` not null
- `event_id` `varchar(64)` not null
- `request_body_json` `jsonb` not null
- `response_status` `integer` null
- `response_body` `text` null
- `attempt_count` `integer` not null
- `next_attempt_at` `timestamptz` null
- `delivered_at` `timestamptz` null
- `created_at` `timestamptz` not null

#### `file_objects`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `bucket` `varchar(64)` not null
- `object_key` `varchar(255)` not null
- `content_type` `varchar(120)` not null
- `size_bytes` `bigint` not null
- `checksum_sha256` `varchar(64)` not null
- `created_by_user_id` fk -> `users.id`
- `created_at` `timestamptz` not null

Constraints:

- unique `(bucket, object_key)`

### Reliability support

#### `idempotency_keys`

- `id` primary key
- `workspace_id` fk -> `workspaces.id`
- `request_method` `varchar(8)` not null
- `request_path` `varchar(255)` not null
- `idempotency_key` `varchar(128)` not null
- `response_status` `integer` null
- `response_body_json` `jsonb` null
- `locked_at` `timestamptz` null
- `expires_at` `timestamptz` not null
- `created_at` `timestamptz` not null

Constraints:

- unique `(workspace_id, request_method, request_path, idempotency_key)`

## ClickHouse tables

### `request_events`

- append-only runtime events derived from `requests`
- partition by month on `created_at`
- primary sort key `(workspace_id, created_at, request_id)`
- columns mirror request latency, token, cost, status, provider, model, prompt, and variant dimensions

### `span_events`

- append-only trace/span facts
- primary sort key `(workspace_id, trace_id, started_at, span_id)`

### `eval_metrics_daily`

- materialized daily aggregate for evaluation quality trends by workspace, pipeline, prompt version, and evaluator

## Index strategy summary

- Time-descending indexes on all primary list views
- GIN indexes on JSONB metadata used in filters
- Unique constraints on natural identifiers such as workspace slug, prompt name per workspace, label name per workspace, and evaluator order per pipeline
- Composite indexes aligned to tenant-first query patterns

## Soft delete policy

- `users`, `workspaces`, `prompt_templates`, `datasets`, `agents`, and secrets support soft delete
- Requests, traces, audit logs, and webhook deliveries are immutable append records

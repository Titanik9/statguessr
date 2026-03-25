# Deployment

## Local stack

The intended local stack is started with Docker Compose and includes:

- `web` for the Next.js console
- `api` for FastAPI
- `worker` for Celery background jobs
- `postgres`
- `redis`
- `clickhouse`
- `minio`
- `mailpit`

## Environment variables

### Shared

- `APP_ENV`
- `PUBLIC_BASE_URL`
- `ENCRYPTION_KEY`

### API

- `DATABASE_URL`
- `REDIS_URL`
- `CLICKHOUSE_URL`
- `S3_ENDPOINT`
- `S3_ACCESS_KEY`
- `S3_SECRET_KEY`
- `S3_BUCKET`
- `JWT_SECRET`
- `MAGIC_LINK_TTL_MINUTES`
- `SESSION_TTL_HOURS`
- `MAIL_FROM`
- `SMTP_HOST`
- `SMTP_PORT`
- `AUTH_DEV_PREVIEW`

### Web

- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_APP_NAME`

## Persistence

- PostgreSQL volume for transactional state
- ClickHouse volume for analytics storage
- MinIO volume for uploaded assets and exports

## Production notes

- Place the web console and API behind a reverse proxy with TLS
- Supply strong operator-managed `JWT_SECRET` and `ENCRYPTION_KEY` values
- Rotate API keys and webhook signing secrets periodically
- Route email through a real SMTP provider instead of Mailpit
- Add managed backups for PostgreSQL, ClickHouse, and MinIO
- Scale worker replicas independently from the API

## Kubernetes-ready posture

The repository is Compose-first, but the separation between web, API, worker, Redis, PostgreSQL, ClickHouse, and MinIO is intentionally service-oriented so each component can later map to a deployment, stateful set, or managed service without reorganizing the codebase.

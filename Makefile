SHELL := /bin/zsh

.PHONY: web-dev api-dev api-test api-migrate ts-sdk-build py-sdk-build compose-up compose-down

web-dev:
	npm run dev:web

api-dev:
	cd apps/api && python3 -m venv .venv && . .venv/bin/activate && pip install -e .[dev] && uvicorn relay_console.main:app --reload --app-dir src

api-test:
	cd apps/api && python3 -m venv .venv && . .venv/bin/activate && pip install -e .[dev] && pytest

api-migrate:
	cd apps/api && python3 -m venv .venv && . .venv/bin/activate && pip install -e .[dev] && alembic upgrade head

ts-sdk-build:
	npm run build:sdk

py-sdk-build:
	cd packages/py-sdk && python3 -m venv .venv && . .venv/bin/activate && pip install build && python -m build

compose-up:
	docker compose -f infra/compose/docker-compose.yml up --build

compose-down:
	docker compose -f infra/compose/docker-compose.yml down -v

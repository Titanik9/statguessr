from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from relay_console.api.router import api_router
from relay_console.core.config import get_settings
from relay_console.db.session import initialize_database


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.auto_migrate_on_boot:
        initialize_database()
    yield


app = FastAPI(
    title="Relay Console API",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or request.headers.get("x-correlation-id")
    if not request_id:
        from relay_console.core.security import generate_id

        request_id = f"req_{generate_id()}"
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


@app.exception_handler(ValueError)
async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})

app.include_router(api_router, prefix="/v1")

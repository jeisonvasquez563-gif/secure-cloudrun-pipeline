"""Minimal FastAPI service used to demonstrate a secure delivery pipeline."""

import os
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

app = FastAPI(
    title="secure-cloudrun-pipeline",
    docs_url=None,  # no interactive docs exposed by default
    redoc_url=None,
    openapi_url=None,
)

APP_VERSION = os.getenv("APP_VERSION", "dev")

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
}


@app.middleware("http")
async def add_security_headers(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = await call_next(request)
    for name, value in SECURITY_HEADERS.items():
        response.headers.setdefault(name, value)
    return response


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION}

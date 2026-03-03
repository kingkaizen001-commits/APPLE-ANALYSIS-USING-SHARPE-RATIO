import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import API_PREFIX, API_VERSION, PRODUCT_NAME, PRODUCT_TAGLINE
from app.core.logging import RequestIdAdapter, setup_logging

setup_logging()
logger = logging.getLogger("bridgaton.api")

app = FastAPI(title=f"{PRODUCT_NAME} — {PRODUCT_TAGLINE}", version=API_VERSION)
app.include_router(router, prefix=API_PREFIX)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    started = time.perf_counter()

    response = await call_next(request)

    duration_ms = (time.perf_counter() - started) * 1000
    adapter = RequestIdAdapter(logger, {"request_id": request_id})
    adapter.info(
        "%s %s -> %s (%.2fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    response.headers["x-request-id"] = request_id
    response.headers["x-response-time-ms"] = f"{duration_ms:.2f}"
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = request.headers.get("x-request-id", "-")
    adapter = RequestIdAdapter(logger, {"request_id": request_id})
    adapter.exception("Unhandled server error at %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": request_id},
    )

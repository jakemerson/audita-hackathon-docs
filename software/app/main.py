"""Aplicação FastAPI do Audita."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.api.audit_routes import router as audit_router
from app.services.session_config import key_store

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
load_dotenv(BASE_DIR.parent / ".env")
key_store.set(os.getenv("OPENAI_API_KEY"))

app = FastAPI(
    title="Audita API",
    version="1.0.0",
    description="Apoio à auditoria de receitas monofásicas no Simples Nacional.",
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Dados de entrada inválidos.", "details": exc.errors(include_context=False)},
    )


class ApiKeyInput(BaseModel):
    api_key: str = Field(default="", max_length=256)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "Audita",
        "ai_mode": "openai" if key_store.configured else "fallback-local",
        "key_configured": key_store.configured,
    }


@app.post("/api/config/set-key")
def set_key(payload: ApiKeyInput):
    configured = key_store.set(payload.api_key)
    return {
        "configured": configured,
        "mode": "openai" if configured else "fallback-local",
        "message": "Chave mantida apenas na memória deste processo." if configured else "Modo local ativado.",
    }


app.include_router(audit_router)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    html = STATIC_DIR / "index.html"
    if html.exists():
        return FileResponse(html)
    return JSONResponse({"service": "Audita", "status": "frontend em preparação"})

"""Rotas de auditoria, demonstração, Copilot e relatórios."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path, PurePosixPath
import re
from zipfile import BadZipFile, ZipFile, is_zipfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field, ValidationError

from app.core.nfe_parser import NFeParseError, audit_xml_batch
from app.models.nfe_models import AuditContext, AuditSummary
from app.services.openai_auditor import generate_audit_opinion
from app.services.session_config import key_store

router = APIRouter(prefix="/api", tags=["auditoria"])

MAX_UPLOAD_BYTES = 25 * 1024 * 1024
MAX_SINGLE_FILE_BYTES = 10 * 1024 * 1024
MAX_XML_FILES = 30
MAX_COMPRESSION_RATIO = 100


def _safe_zip_xmls(name: str, content: bytes) -> list[tuple[str, bytes]]:
    if not is_zipfile(BytesIO(content)):
        raise HTTPException(status_code=400, detail=f"{name}: ZIP inválido.")
    extracted: list[tuple[str, bytes]] = []
    total = 0
    try:
        with ZipFile(BytesIO(content)) as archive:
            members = archive.infolist()
            if len(members) > MAX_XML_FILES:
                raise HTTPException(status_code=400, detail="ZIP excede o limite de 30 membros.")
            for info in members:
                path = PurePosixPath(info.filename.replace("\\", "/"))
                if info.is_dir():
                    continue
                if path.is_absolute() or ".." in path.parts:
                    raise HTTPException(status_code=400, detail="ZIP contém caminho inseguro.")
                if path.suffix.casefold() != ".xml":
                    raise HTTPException(status_code=400, detail="ZIP deve conter somente XMLs.")
                if info.file_size > MAX_SINGLE_FILE_BYTES:
                    raise HTTPException(status_code=413, detail="XML compactado excede 10 MB.")
                if info.compress_size == 0 and info.file_size > 0:
                    raise HTTPException(status_code=400, detail="Razão de compactação insegura.")
                if info.compress_size and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
                    raise HTTPException(status_code=400, detail="Possível ZIP bomb detectado.")
                total += info.file_size
                if total > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="Conteúdo descompactado excede 25 MB.")
                extracted.append((path.name, archive.read(info)))
    except BadZipFile as exc:
        raise HTTPException(status_code=400, detail=f"{name}: ZIP inválido.") from exc
    if not extracted:
        raise HTTPException(status_code=400, detail="ZIP não contém XMLs.")
    return extracted


async def _collect_uploads(files: list[UploadFile]) -> list[tuple[str, bytes]]:
    if not files or len(files) > MAX_XML_FILES:
        raise HTTPException(status_code=400, detail="Envie entre 1 e 30 arquivos XML/ZIP.")
    xml_files: list[tuple[str, bytes]] = []
    total = 0
    for upload in files:
        filename = Path(upload.filename or "arquivo").name
        suffix = Path(filename).suffix.casefold()
        if suffix not in {".xml", ".zip"}:
            raise HTTPException(status_code=400, detail=f"{filename}: extensão não aceita.")
        content = await upload.read(MAX_UPLOAD_BYTES + 1)
        total += len(content)
        if total > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="Lote excede o limite de 25 MB.")
        if suffix == ".xml":
            if len(content) > MAX_SINGLE_FILE_BYTES:
                raise HTTPException(status_code=413, detail=f"{filename}: XML excede 10 MB.")
            xml_files.append((filename, content))
        else:
            xml_files.extend(_safe_zip_xmls(filename, content))
        if len(xml_files) > MAX_XML_FILES:
            raise HTTPException(status_code=400, detail="Lote excede 30 XMLs.")
    return xml_files


def _context(rbt12: str, pgdas_segregated: bool, period: str) -> AuditContext:
    if not re.fullmatch(r"\d{4}-\d{2}", period):
        raise HTTPException(status_code=422, detail="Período deve usar AAAA-MM.")
    try:
        return AuditContext(rbt12=rbt12, annex="I", pgdas_segregated=pgdas_segregated, period=period)
    except (ValidationError, ValueError) as exc:
        raise HTTPException(status_code=422, detail="RBT12 deve estar entre zero e R$ 3,6 milhões.") from exc


def _response(summary: AuditSummary) -> dict:
    opinion = generate_audit_opinion(summary, key_store.get())
    return {
        "report": summary.public_dict(),
        "opinion": opinion.model_dump(mode="json"),
        "meta": {
            "product": "Audita",
            "calculation_engine": "determinístico-v1",
            "ai_mode": opinion.source,
            "disclaimer": "Potencial estimado sujeito a documentos, PGDAS-D e validação do contador.",
        },
    }


@router.post("/audit/upload")
async def upload_audit(
    files: list[UploadFile] = File(...),
    rbt12: str = Form(...),
    pgdas_segregated: bool = Form(False),
    period: str = Form("2026-08"),
):
    xml_files = await _collect_uploads(files)
    try:
        summary = audit_xml_batch(xml_files, _context(rbt12, pgdas_segregated, period))
    except NFeParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _response(summary)


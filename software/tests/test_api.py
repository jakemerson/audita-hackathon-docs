from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.session_config import key_store
from tests.conftest import make_xml


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_dynamic_key():
    key_store.set(None)
    yield
    key_store.set(None)


def test_health_reports_local_mode_without_secret():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["ai_mode"] == "fallback-local"
    assert "api_key" not in response.text


def test_dynamic_key_response_never_echoes_value():
    secret = "sk-test-" + "x" * 40
    response = client.post("/api/config/set-key", json={"api_key": secret})
    assert response.status_code == 200
    assert response.json()["configured"] is True
    assert secret not in response.text


def test_upload_returns_deterministic_audit_report():
    response = client.post(
        "/api/audit/upload",
        data={"rbt12": "1800000", "pgdas_segregated": "false", "period": "2026-08"},
        files=[("files", ("nota.xml", make_xml(), "application/xml"))],
    )
    assert response.status_code == 200
    body = response.json()
    assert body["report"]["estimated_overpayment"] == "14.65"
    assert body["report"]["findings"][0]["status"] == "CONFIRMADO"
    assert body["meta"]["calculation_engine"] == "determinístico-v1"


def test_upload_rejects_unknown_extension():
    response = client.post(
        "/api/audit/upload",
        data={"rbt12": "1800000"},
        files=[("files", ("nota.txt", b"not xml", "text/plain"))],
    )
    assert response.status_code == 400


def test_zip_rejects_path_traversal():
    payload = BytesIO()
    with ZipFile(payload, "w", ZIP_DEFLATED) as archive:
        archive.writestr("../nota.xml", make_xml())
    response = client.post(
        "/api/audit/upload",
        data={"rbt12": "1800000"},
        files=[("files", ("lote.zip", payload.getvalue(), "application/zip"))],
    )
    assert response.status_code == 400
    assert "inseguro" in response.text


def test_zip_accepts_three_hundred_xmls():
    payload = BytesIO()
    with ZipFile(payload, "w", ZIP_DEFLATED) as archive:
        for index in range(300):
            archive.writestr(f"nota-{index:03d}.xml", make_xml())
    response = client.post(
        "/api/audit/upload",
        data={"rbt12": "1800000", "period": "2026-08"},
        files=[("files", ("lote-300.zip", payload.getvalue(), "application/zip"))],
    )
    assert response.status_code == 200
    assert response.json()["report"]["invoice_count"] == 300


def test_zip_rejects_more_than_five_hundred_xmls_with_clear_message():
    payload = BytesIO()
    with ZipFile(payload, "w", ZIP_DEFLATED) as archive:
        for index in range(501):
            archive.writestr(f"nota-{index:03d}.xml", make_xml())
    response = client.post(
        "/api/audit/upload",
        data={"rbt12": "1800000"},
        files=[("files", ("lote-501.zip", payload.getvalue(), "application/zip"))],
    )
    assert response.status_code == 400
    assert "mais de 500 XMLs" in response.text


def test_copilot_route_returns_sources():
    response = client.post("/api/audit/copilot", json={"question": "Como retificar o PGDAS?"})
    assert response.status_code == 200
    assert response.json()["sources"]
    assert response.json()["source"] == "local"


def test_report_download_routes_stream_valid_files():
    audit = client.post(
        "/api/audit/upload",
        data={"rbt12": "1800000"},
        files=[("files", ("nota.xml", make_xml(), "application/xml"))],
    ).json()["report"]
    excel = client.post("/api/export/excel", json={"report": audit})
    pdf = client.post("/api/export/pdf", json={"report": audit})
    assert excel.status_code == 200 and excel.content.startswith(b"PK")
    assert pdf.status_code == 200 and pdf.content.startswith(b"%PDF")

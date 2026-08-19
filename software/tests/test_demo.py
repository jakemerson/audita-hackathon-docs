from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from fastapi.testclient import TestClient

from app.core.nfe_parser import parse_nfe_xml
from app.main import app


SAMPLES = Path(__file__).resolve().parents[1] / "sample_invoices"
client = TestClient(app)


def test_five_workshop_fixtures_are_synthetic_and_parseable():
    files = sorted(SAMPLES.glob("oficina_*.xml"))
    assert len(files) == 5
    documents = [parse_nfe_xml(path.read_bytes(), path.name) for path in files]
    assert all(document.synthetic_fixture for document in documents)
    assert {document.items[0].ncm for document in documents} == {"87083090", "87088000", "84212300", "85111000", "40111000"}


def test_demo_endpoint_is_exactly_1840_and_never_promises_credit():
    response = client.post("/api/audit/demo-oficina")
    assert response.status_code == 200
    body = response.json()
    assert body["report"]["estimated_overpayment"] == "1840.00"
    assert body["report"]["synthetic_simulation"] is True
    assert "sujeito" in body["meta"]["disclaimer"]


def test_physical_zip_contains_only_the_five_workshop_xmls():
    archive_path = SAMPLES / "lote_oficina_mecanica_5_notas.zip"
    with ZipFile(archive_path) as archive:
        assert len(archive.namelist()) == 5
        assert all(name.endswith(".xml") for name in archive.namelist())
        assert all(b"FIXTURE SINTETICA AUDITA" in archive.read(name) for name in archive.namelist())


def test_zip_upload_reproduces_demo_estimate():
    payload = (SAMPLES / "lote_oficina_mecanica_5_notas.zip").read_bytes()
    response = client.post(
        "/api/audit/upload",
        data={"rbt12": "1800000", "pgdas_segregated": "false", "period": "2026-08"},
        files=[("files", ("lote.zip", BytesIO(payload), "application/zip"))],
    )
    assert response.status_code == 200
    assert response.json()["report"]["estimated_overpayment"] == "1840.00"


def test_extra_segment_fixtures_cover_beverage_and_pharmacy():
    beer = parse_nfe_xml((SAMPLES / "extra_cervejaria.xml").read_bytes())
    pharmacy = parse_nfe_xml((SAMPLES / "extra_farmacia.xml").read_bytes())
    assert beer.items[0].ncm.startswith("2203")
    assert pharmacy.items[0].ncm.startswith("3004")

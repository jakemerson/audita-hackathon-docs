from pathlib import Path

from fastapi.testclient import TestClient
from lxml import html

from app.main import app


STATIC = Path(__file__).resolve().parents[1] / "app" / "static"


def _document():
    return html.fromstring((STATIC / "index.html").read_text(encoding="utf-8"))


def test_spa_has_unique_ids_and_portuguese_language():
    document = _document()
    ids = document.xpath("//*[@id]/@id")
    assert len(ids) == len(set(ids))
    assert document.get("lang") == "pt-BR"


def test_dropzone_and_dialog_are_keyboard_discoverable():
    document = _document()
    dropzone = document.get_element_by_id("dropzone")
    assert dropzone.get("role") == "button"
    assert dropzone.get("tabindex") == "0"
    assert document.get_element_by_id("keyModal").tag == "dialog"
    assert document.get_element_by_id("openKeyModal").get("aria-label") == "Configurar OpenAI"
    assert document.get_element_by_id("closeCopilot").get("aria-label")


def test_every_form_control_has_label_or_accessible_name():
    document = _document()
    label_targets = set(document.xpath("//label/@for"))
    for control in document.xpath("//input|//textarea|//select"):
        control_id = control.get("id")
        wrapped = bool(control.xpath("ancestor::label"))
        assert wrapped or control_id in label_targets or control.get("aria-label"), control_id


def test_styles_cover_focus_responsiveness_and_reduced_motion():
    styles = (STATIC / "styles.css").read_text(encoding="utf-8")
    assert ":focus-visible" in styles
    assert "prefers-reduced-motion" in styles
    assert "@media(max-width:620px)" in styles
    assert "overflow-x:hidden" in styles
    assert ".evidence-grid>*{min-width:0}" in styles
    assert ".evidence-grid{grid-template-columns:minmax(0,1fr)}" in styles


def test_javascript_binds_critical_controls_and_avoids_inner_html():
    script = (STATIC / "app.js").read_text(encoding="utf-8")
    for selector in ("#demoButton", "#itemSearch", "#openCopilot", "#downloadExcel", "#downloadPdf"):
        assert selector in script
    assert ".innerHTML" not in script
    assert "prefers-reduced-motion" in script
    assert 'modal.addEventListener("cancel"' in script
    assert 'modal.addEventListener("keydown"' in script
    assert 'event.key !== "Escape"' in script


def test_copy_uses_audita_and_responsible_estimate_language():
    copy = " ".join(_document().itertext())
    assert "AuditaPix" not in copy
    assert "Audita" in copy
    assert "Não é crédito garantido" in copy
    assert "Simulação sintética" in copy


def test_fastapi_serves_spa_and_static_assets():
    client = TestClient(app)
    page = client.get("/")
    styles = client.get("/static/styles.css")
    script = client.get("/static/app.js")
    assert page.status_code == styles.status_code == script.status_code == 200
    assert "Do XML" in page.text
    assert styles.headers["content-type"].startswith("text/css")
    assert "renderResults" in script.text

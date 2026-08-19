from decimal import Decimal

import pytest

from app.core.nfe_parser import NFeParseError, audit_xml_batch, parse_nfe_xml
from tests.conftest import make_xml


def test_parses_wrapped_namespaced_nfe():
    doc = parse_nfe_xml(make_xml(), "nota.xml")
    assert doc.number == "1001"
    assert doc.issuer.name == "OFICINA FIXTURE"
    assert doc.items[0].ncm == "87083090"
    assert doc.items[0].pis_cst == "01"
    assert doc.items[0].csosn == "102"
    assert doc.synthetic_fixture is True


def test_parses_unwrapped_nfe_with_different_namespace():
    doc = parse_nfe_xml(make_xml(namespace="urn:sefaz:custom", wrapped=False))
    assert doc.model == "55"
    assert doc.total_products == Decimal("1000.00")


def test_rejects_malformed_xml():
    with pytest.raises(NFeParseError, match="malformado"):
        parse_nfe_xml(b"<NFe><broken>", "quebrado.xml")


def test_rejects_doctype_and_entities():
    payload = b'<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>'
    with pytest.raises(NFeParseError, match="entidades"):
        parse_nfe_xml(payload)


def test_batch_consolidates_sales_and_flags_synthetic(context):
    summary = audit_xml_batch(
        [("a.xml", make_xml(value="1000.00")), ("b.xml", make_xml(value="2000.00"))],
        context,
    )
    assert summary.invoice_count == 2
    assert summary.audited_revenue == Decimal("3000.00")
    assert summary.confirmed_monophase_revenue == Decimal("3000.00")
    assert summary.estimated_overpayment == Decimal("43.95")
    assert summary.synthetic_simulation is True

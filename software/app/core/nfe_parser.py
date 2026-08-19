"""Parser resiliente de NF-e/NFC-e 4.00 sem depender de prefixos XML."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Iterable

from lxml import etree

from app.core.tax_rules import audit_documents
from app.models.nfe_models import AuditContext, NFeDocument, NFeItem, Party


class NFeParseError(ValueError):
    """Erro seguro e apresentável para documento fiscal inválido."""


def _first(node: etree._Element, expression: str) -> etree._Element | None:
    values = node.xpath(expression)
    return values[0] if values else None


def _text(node: etree._Element | None, child_name: str, default: str = "") -> str:
    if node is None:
        return default
    child = _first(node, f"./*[local-name()='{child_name}']")
    return (child.text or "").strip() if child is not None else default


def _decimal(value: str, field: str) -> Decimal:
    try:
        return Decimal(value or "0")
    except InvalidOperation as exc:
        raise NFeParseError(f"Campo numérico inválido em {field}.") from exc


def _parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _tax_code(tax_root: etree._Element | None, tax_name: str, code: str) -> str | None:
    if tax_root is None:
        return None
    node = _first(
        tax_root,
        f".//*[local-name()='{tax_name}']//*[local-name()='{code}']",
    )
    return (node.text or "").strip() if node is not None else None


def parse_nfe_xml(content: bytes, filename: str = "documento.xml") -> NFeDocument:
    if not content or len(content) > 10 * 1024 * 1024:
        raise NFeParseError("XML vazio ou maior que o limite de 10 MB.")
    if b"<!DOCTYPE" in content.upper() or b"<!ENTITY" in content.upper():
        raise NFeParseError("DTD e entidades externas não são aceitas.")
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False, huge_tree=False)
    try:
        root = etree.fromstring(content, parser=parser)
    except (etree.XMLSyntaxError, ValueError) as exc:
        raise NFeParseError(f"{filename}: XML malformado ou inseguro.") from exc

    inf = _first(root, ".//*[local-name()='infNFe']")
    if inf is None and etree.QName(root).localname == "infNFe":
        inf = root
    if inf is None:
        raise NFeParseError(f"{filename}: estrutura infNFe não encontrada.")

    ide = _first(inf, "./*[local-name()='ide']")
    emit = _first(inf, "./*[local-name()='emit']")
    dest = _first(inf, "./*[local-name()='dest']")
    if ide is None or emit is None:
        raise NFeParseError(f"{filename}: cabeçalho ou emitente ausente.")

    issuer = Party(
        tax_id=_text(emit, "CNPJ") or _text(emit, "CPF"),
        name=_text(emit, "xNome", "Emitente não informado"),
        crt=_text(emit, "CRT") or None,
    )
    recipient = Party(
        tax_id=_text(dest, "CNPJ") or _text(dest, "CPF"),
        name=_text(dest, "xNome", "Destinatário não informado"),
    )
    items: list[NFeItem] = []
    for position, det in enumerate(inf.xpath("./*[local-name()='det']"), start=1):
        prod = _first(det, "./*[local-name()='prod']")
        if prod is None:
            continue
        tax = _first(det, "./*[local-name()='imposto']")
        icms_cst = _tax_code(tax, "ICMS", "CST")
        csosn = _tax_code(tax, "ICMS", "CSOSN")
        line_number = int(det.get("nItem") or position)
        items.append(
            NFeItem(
                line_number=line_number,
                product_code=_text(prod, "cProd"),
                description=_text(prod, "xProd", "Produto sem descrição"),
                ncm=_text(prod, "NCM"),
                cfop=_text(prod, "CFOP"),
                quantity=_decimal(_text(prod, "qCom", "1"), "qCom"),
                unit_value=_decimal(_text(prod, "vUnCom"), "vUnCom"),
                product_value=_decimal(_text(prod, "vProd"), "vProd"),
                pis_cst=_tax_code(tax, "PIS", "CST"),
                cofins_cst=_tax_code(tax, "COFINS", "CST"),
                icms_cst=icms_cst,
                csosn=csosn,
            )
        )
    if not items:
        raise NFeParseError(f"{filename}: nenhum item fiscal foi encontrado.")

    raw_text = " ".join(text.strip() for text in inf.itertext() if text and text.strip()).casefold()
    return NFeDocument(
        access_key=(inf.get("Id") or "").removeprefix("NFe"),
        number=_text(ide, "nNF", "Sem número"),
        series=_text(ide, "serie"),
        issued_at=_parse_datetime(_text(ide, "dhEmi") or _text(ide, "dEmi")),
        model=_text(ide, "mod", "55"),
        issuer=issuer,
        recipient=recipient,
        items=items,
        synthetic_fixture="fixture sintetica audita" in raw_text or "fixture sintética audita" in raw_text,
    )


def audit_xml_batch(
    xml_files: Iterable[tuple[str, bytes]],
    context: AuditContext,
):
    documents = [parse_nfe_xml(content, filename) for filename, content in xml_files]
    if not documents:
        raise NFeParseError("Nenhum XML válido foi informado.")
    return audit_documents(documents, context)

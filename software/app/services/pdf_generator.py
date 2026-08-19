"""Memória de cálculo em PDF — deliberadamente não é uma petição."""

from __future__ import annotations

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.models.nfe_models import AuditSummary


def _money(value) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def generate_pdf(summary: AuditSummary) -> bytes:
    output = BytesIO()
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Audita — Memória de cálculo",
        author="Audita",
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Hero", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, textColor=colors.HexColor("#0F172A"), alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle(name="SmallMuted", parent=styles["BodyText"], fontSize=8, textColor=colors.HexColor("#475569"), leading=11))
    styles["Heading2"].textColor = colors.HexColor("#0F172A")
    styles["Heading2"].spaceBefore = 12
    story = [
        Paragraph("AUDITA", styles["Hero"]),
        Paragraph("Memória de cálculo e checklist de validação tributária", styles["Heading2"]),
        Paragraph(
            "DOCUMENTO DE APOIO TÉCNICO — não é petição, parecer jurídico, transmissão ao PGDAS-D ou garantia de crédito/deferimento.",
            styles["SmallMuted"],
        ),
        Spacer(1, 8),
    ]
    if summary.synthetic_simulation:
        story.append(Paragraph("SIMULAÇÃO SINTÉTICA, SEM VALOR FISCAL", styles["Heading3"]))
    data = [
        ["Premissa", "Valor"],
        ["Período", summary.context.period],
        ["RBT12", _money(summary.context.rbt12)],
        ["Faixa Anexo I", str(summary.rate.band)],
        ["Alíquota efetiva DAS", f"{summary.rate.effective_das_rate * 100:.4f}%"],
        ["Fração PIS/Cofins do DAS", f"{summary.rate.pis_cofins_share * 100:.2f}%"],
        ["Alíquota efetiva PIS/Cofins", f"{summary.rate.effective_pis_cofins_rate * 100:.6f}%"],
        ["PGDAS-D já segregado", "Sim — potencial zerado" if summary.context.pgdas_segregated else "Não informado como segregado"],
        ["Potencial estimado", _money(summary.estimated_overpayment)],
    ]
    table = Table(data, colWidths=[72 * mm, 85 * mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([table, Paragraph("Itens auditados", styles["Heading2"])])
    item_data = [["Nota / item", "Produto / NCM", "Status", "Potencial"]]
    for finding in summary.findings:
        item_data.append([
            f"{finding.invoice_number} / {finding.item_number}",
            Paragraph(f"{finding.description}<br/><font size='7'>NCM {finding.ncm}</font>", styles["BodyText"]),
            finding.status.value,
            _money(finding.estimated_overpayment),
        ])
    item_table = Table(item_data, colWidths=[30 * mm, 76 * mm, 30 * mm, 27 * mm], repeatRows=1)
    item_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([
        item_table,
        PageBreak(),
        Paragraph("Base normativa de referência", styles["Heading2"]),
        Paragraph(
            "LC 123/2006, art. 18, § 4º-A, I; CTN, arts. 165 e 168; Resolução CGSN 140/2018; "
            "IN RFB 2.055/2021; Leis 10.147/2000, 10.485/2002 e 13.097/2015; tabelas SPED 4.3.10 e 4.3.11.",
            styles["BodyText"],
        ),
        Paragraph("Checklist antes de qualquer ação", styles["Heading2"]),
        Paragraph("□ Confirmar que os XMLs representam vendas e reconciliar com NFC-e/extrato do período.", styles["BodyText"]),
        Paragraph("□ Validar NCM, descrição, destinação, exceções e vigência de cada item.", styles["BodyText"]),
        Paragraph("□ Conferir segregação efetivamente declarada no PGDAS-D.", styles["BodyText"]),
        Paragraph("□ Confirmar RBT12, faixa, alíquota efetiva e composição de PIS/Cofins.", styles["BodyText"]),
        Paragraph("□ Solicitar validação e assinatura do contador responsável.", styles["BodyText"]),
        Spacer(1, 28),
        Paragraph("__________________________________________<br/>Contador responsável — CRC / data", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Quando houver manifestação jurídica, solicite revisão de advogado habilitado.", styles["SmallMuted"]),
    ])
    doc.build(story)
    return output.getvalue()

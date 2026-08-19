"""Motor tributário determinístico, versionado e explicável do Audita.

O conjunto abaixo cobre o MVP e a demonstração. Ele não é apresentado como uma
lista universal: regras amplas, exceções ``Ex``, descrição, destinação e vigência
devem ser revistas contra as tabelas 4.3.10/4.3.11 do SPED.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import re

from app.models.nfe_models import (
    AuditContext,
    AuditFinding,
    AuditStatus,
    NFeDocument,
    NFeItem,
    RateBreakdown,
    RuleEvidence,
)

MONEY = Decimal("0.01")
PIS_COFINS_SHARE_ANNEX_I = Decimal("0.155")
COMMON_PIS_COFINS_CSTS = {"01", "02", "49", "99"}


@dataclass(frozen=True)
class AnnexBand:
    ceiling: Decimal
    nominal_rate: Decimal
    deduction: Decimal


ANNEX_I_BANDS = (
    AnnexBand(Decimal("180000"), Decimal("0.04"), Decimal("0")),
    AnnexBand(Decimal("360000"), Decimal("0.073"), Decimal("5940")),
    AnnexBand(Decimal("720000"), Decimal("0.095"), Decimal("13860")),
    AnnexBand(Decimal("1800000"), Decimal("0.107"), Decimal("22500")),
    AnnexBand(Decimal("3600000"), Decimal("0.143"), Decimal("87300")),
)


@dataclass(frozen=True)
class TaxRule:
    rule_id: str
    pattern: str
    match_type: str
    segment: str
    description: str
    legal_source: str
    legal_url: str
    valid_from: str
    exceptions: tuple[str, ...] = ()
    description_required: tuple[str, ...] = ()
    caveats: tuple[str, ...] = ()


PLANALTO_10485 = "https://www.planalto.gov.br/ccivil_03/leis/2002/l10485compilado.htm"
PLANALTO_10147 = "https://www.planalto.gov.br/ccivil_03/leis/l10147.htm"
PLANALTO_13097 = "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13097.htm"

RULES: tuple[TaxRule, ...] = (
    TaxRule("AUTO-8708", "8708", "prefix", "Autopeças", "Partes e acessórios de veículos", "Lei 10.485/2002, Anexo I", PLANALTO_10485, "2002-07-03"),
    TaxRule("AUTO-842123", "84212300", "exact", "Autopeças", "Filtros de óleo para motores", "Lei 10.485/2002, Anexo I", PLANALTO_10485, "2002-07-03"),
    TaxRule("AUTO-842131", "84213100", "exact", "Autopeças", "Filtros de entrada de ar", "Lei 10.485/2002, Anexo I", PLANALTO_10485, "2002-07-03"),
    TaxRule("AUTO-8511", "8511", "prefix", "Autopeças", "Aparelhos de ignição e partes", "Lei 10.485/2002, Anexo I", PLANALTO_10485, "2002-07-03"),
    TaxRule("AUTO-4011", "4011", "prefix", "Pneus", "Pneus novos de borracha", "Lei 10.485/2002, arts. 5º e 6º", PLANALTO_10485, "2002-07-03", caveats=("Produtos usados não estão abrangidos.",)),
    TaxRule("AUTO-850710", "85071000", "exact", "Autopeças", "Acumuladores de chumbo para partida", "Lei 10.485/2002, Anexo I", PLANALTO_10485, "2002-07-03"),
    TaxRule("FARMA-3001", "3001", "prefix", "Medicamentos", "Produtos farmacêuticos da posição 30.01", "Lei 10.147/2000, arts. 1º e 2º", PLANALTO_10147, "2000-12-22"),
    TaxRule("FARMA-3003", "3003", "prefix", "Medicamentos", "Medicamentos da posição 30.03", "Lei 10.147/2000, arts. 1º e 2º", PLANALTO_10147, "2000-12-22", exceptions=("30039056",)),
    TaxRule("FARMA-3004", "3004", "prefix", "Medicamentos", "Medicamentos da posição 30.04", "Lei 10.147/2000, arts. 1º e 2º", PLANALTO_10147, "2000-12-22", exceptions=("30049046",)),
    TaxRule("BEAUTY-3303", "3303", "prefix", "Perfumaria", "Perfumes e águas de colônia", "Lei 10.147/2000, arts. 1º e 2º", PLANALTO_10147, "2000-12-22"),
    TaxRule("BEAUTY-3304", "3304", "prefix", "Cosméticos", "Produtos de beleza ou maquiagem", "Lei 10.147/2000, arts. 1º e 2º", PLANALTO_10147, "2000-12-22"),
    TaxRule("BEAUTY-3305", "3305", "prefix", "Higiene pessoal", "Preparações capilares", "Lei 10.147/2000, arts. 1º e 2º", PLANALTO_10147, "2000-12-22"),
    TaxRule("DRINK-2201", "2201", "prefix", "Bebidas frias", "Águas no escopo legal", "Lei 13.097/2015, arts. 14 e 28", PLANALTO_13097, "2015-05-01", description_required=("agua", "água"), caveats=("Exige varejista não industrial/importador e validação da descrição legal.",)),
    TaxRule("DRINK-2202", "2202", "prefix", "Bebidas frias", "Bebidas não alcoólicas no escopo legal", "Lei 13.097/2015, arts. 14 e 28", PLANALTO_13097, "2015-05-01", description_required=("refrigerante", "energetico", "energético", "cha", "chá", "refresco", "cerveja sem alcool", "cerveja sem álcool"), caveats=("Nem todo produto da posição 22.02 está abrangido.",)),
    TaxRule("DRINK-2203", "2203", "prefix", "Bebidas frias", "Cervejas de malte", "Lei 13.097/2015, arts. 14 e 28", PLANALTO_13097, "2015-05-01", caveats=("Exige varejista não industrial/importador.",)),
)


def normalize_ncm(value: str) -> str:
    return re.sub(r"\D", "", value or "")[:8]


def calculate_annex_i_rate(rbt12: Decimal | str | float) -> RateBreakdown:
    revenue = Decimal(str(rbt12))
    if revenue <= 0:
        raise ValueError("RBT12 deve ser maior que zero.")
    band = next((entry for entry in ANNEX_I_BANDS if revenue <= entry.ceiling), None)
    if band is None:
        raise ValueError("MVP suporta o Anexo I até R$ 3,6 milhões (faixas 1 a 5).")
    effective = ((revenue * band.nominal_rate) - band.deduction) / revenue
    pis_cofins = effective * PIS_COFINS_SHARE_ANNEX_I
    return RateBreakdown(
        band=ANNEX_I_BANDS.index(band) + 1,
        nominal_rate=band.nominal_rate,
        deduction=band.deduction,
        effective_das_rate=effective,
        pis_cofins_share=PIS_COFINS_SHARE_ANNEX_I,
        effective_pis_cofins_rate=pis_cofins,
    )


def _match_rule(item: NFeItem) -> tuple[TaxRule | None, AuditStatus, str, list[str]]:
    ncm = normalize_ncm(item.ncm)
    description = item.description.casefold()
    for rule in RULES:
        matched = ncm == rule.pattern if rule.match_type == "exact" else ncm.startswith(rule.pattern)
        if not matched:
            continue
        if any(ncm.startswith(exc) for exc in rule.exceptions):
            return rule, AuditStatus.NAO_ENQUADRADO, "Exceção legal expressa para este desdobramento.", list(rule.caveats)
        if rule.rule_id == "AUTO-4011" and any(term in description for term in ("usado", "recauchutado", "remanufaturado")):
            return rule, AuditStatus.NAO_ENQUADRADO, "Descrição indica produto usado, excluído pelo art. 6º.", list(rule.caveats)
        if rule.description_required and not any(term in description for term in rule.description_required):
            return rule, AuditStatus.REVISAR, "NCM compatível, mas a descrição/destinação legal não foi comprovada.", list(rule.caveats)
        return rule, AuditStatus.CONFIRMADO, "NCM e descrição compatíveis com a regra versionada do MVP.", list(rule.caveats)
    return None, AuditStatus.NAO_ENQUADRADO, "Nenhuma regra versionada do MVP correspondeu ao NCM.", ["Consulte as tabelas SPED 4.3.10 e 4.3.11 vigentes na operação."]


def classify_item(item: NFeItem, invoice_number: str, context: AuditContext) -> AuditFinding:
    rule, status, reason, caveats = _match_rule(item)
    pending: list[str] = []
    if not item.is_sale:
        status = AuditStatus.REVISAR if status is AuditStatus.CONFIRMADO else status
        pending.append("Documento não tem CFOP de saída; XML de compra isolado não comprova receita nem pagamento a maior.")
    csts = {value for value in (item.pis_cst, item.cofins_cst) if value}
    if csts & COMMON_PIS_COFINS_CSTS:
        signal = "CST de PIS/Cofins sugere tributação comum; é apenas um sinal a conciliar com vendas e PGDAS-D."
    elif "04" in csts:
        signal = "CST 04 sinaliza operação monofásica/revenda a alíquota zero."
    else:
        signal = "CST de PIS/Cofins ausente ou inconclusivo; requer validação documental."
    if item.csosn:
        pending.append(f"CSOSN {item.csosn} pertence ao ICMS e não decide PIS/Cofins.")
    if context.pgdas_segregated:
        pending.append("Receita informada como já segregada no PGDAS-D; potencial calculado em zero.")
    if status is AuditStatus.REVISAR:
        pending.append("Confirmar descrição, destinação, papel do vendedor e vigência da NCM.")

    estimated = Decimal("0")
    if status is AuditStatus.CONFIRMADO and item.is_sale and not context.pgdas_segregated:
        rate = calculate_annex_i_rate(context.rbt12).effective_pis_cofins_rate
        estimated = (item.product_value * rate).quantize(MONEY, rounding=ROUND_HALF_UP)

    evidence = None
    if rule:
        evidence = RuleEvidence(
            rule_id=rule.rule_id,
            legal_source=rule.legal_source,
            legal_url=rule.legal_url,
            valid_from=rule.valid_from,
            match_type=rule.match_type,
            reason=reason,
            caveats=caveats,
        )
    return AuditFinding(
        invoice_number=invoice_number,
        item_number=item.line_number,
        product_code=item.product_code,
        description=item.description,
        ncm=normalize_ncm(item.ncm),
        cfop=item.cfop,
        product_value=item.product_value,
        pis_cst=item.pis_cst,
        cofins_cst=item.cofins_cst,
        csosn=item.csosn,
        status=status,
        segment=rule.segment if rule else "Fora do catálogo MVP",
        signal=signal,
        estimated_overpayment=estimated,
        evidence=evidence,
        pending_checks=pending,
    )


def audit_documents(documents: list[NFeDocument], context: AuditContext):
    from app.models.nfe_models import AuditSummary

    rate = calculate_annex_i_rate(context.rbt12)
    findings = [classify_item(item, doc.number, context) for doc in documents for item in doc.items]
    audited = sum((item.product_value for doc in documents for item in doc.items if item.is_sale), Decimal("0"))
    confirmed = sum((f.product_value for f in findings if f.status is AuditStatus.CONFIRMADO and f.cfop[:1] in {"5", "6", "7"}), Decimal("0"))
    review = sum((f.product_value for f in findings if f.status is AuditStatus.REVISAR), Decimal("0"))
    potential = sum((f.estimated_overpayment for f in findings), Decimal("0")).quantize(MONEY)
    warnings = [
        "Estimativa de apoio técnico: não é crédito garantido, petição ou parecer jurídico.",
        "Concilie as vendas com o PGDAS-D e valide regras, vigência e documentos com o contador.",
        "A classificação usa um catálogo versionado do MVP, não uma lista legal universal.",
    ]
    return AuditSummary(
        context=context,
        rate=rate,
        invoice_count=len(documents),
        item_count=len(findings),
        audited_revenue=audited,
        confirmed_monophase_revenue=confirmed,
        review_revenue=review,
        estimated_overpayment=potential,
        findings=findings,
        warnings=warnings,
        synthetic_simulation=bool(documents) and all(doc.synthetic_fixture for doc in documents),
    )

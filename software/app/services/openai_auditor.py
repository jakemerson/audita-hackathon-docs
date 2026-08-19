"""Explicação opcional por IA; números e classificação nunca saem do motor local."""

from __future__ import annotations

import json
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field

from app.models.nfe_models import AuditSummary


class AuditOpinion(BaseModel):
    resumo: str
    fundamentacao: list[str] = Field(min_length=1)
    plano_acao: list[str] = Field(min_length=1)
    alertas: list[str] = Field(min_length=1)
    source: Literal["openai", "local"] = "local"


def usable_key(api_key: str | None) -> bool:
    if not api_key:
        return False
    normalized = api_key.strip()
    return len(normalized) > 20 and normalized not in {"sua_chave_openai_aqui", "placeholder"}


def local_opinion(summary: AuditSummary) -> AuditOpinion:
    amount = f"R$ {summary.estimated_overpayment:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return AuditOpinion(
        resumo=(
            f"O motor determinístico encontrou um potencial estimado de {amount}. "
            "O valor não é crédito garantido: depende da conciliação entre receitas de venda, "
            "segregação no PGDAS-D, vigência e condições de cada regra."
        ),
        fundamentacao=[
            "LC 123/2006, art. 18, § 4º-A, I: segregação de receitas sujeitas à tributação concentrada.",
            "Leis 10.147/2000, 10.485/2002 e 13.097/2015: regras por produto, descrição, papel e período.",
            "CTN, arts. 165 e 168, Resolução CGSN 140/2018 e IN RFB 2.055/2021: revisão e restituição sujeitas a requisitos e prazo legal.",
        ],
        plano_acao=[
            "Conciliar XMLs de venda e NFC-e com o extrato mensal e o PGDAS-D.",
            "Validar NCM, descrição, destinação, CST de PIS/Cofins e vigência com o contador.",
            "Somente após validação, avaliar retificação e eventual pedido pelo canal aplicável.",
        ],
        alertas=[
            "XML de compra, NCM ou CST isolado não comprova pagamento indevido.",
            "CSOSN é código de ICMS e não substitui o CST de PIS/Cofins.",
            "A transição para CBS a partir de 2027 exige regras por período para fatos geradores legados.",
        ],
        source="local",
    )


def generate_audit_opinion(summary: AuditSummary, api_key: str | None = None) -> AuditOpinion:
    fallback = local_opinion(summary)
    if not usable_key(api_key):
        return fallback
    deterministic = {
        "invoice_count": summary.invoice_count,
        "audited_revenue": str(summary.audited_revenue),
        "confirmed_monophase_revenue": str(summary.confirmed_monophase_revenue),
        "estimated_overpayment": str(summary.estimated_overpayment),
        "effective_pis_cofins_rate": str(summary.rate.effective_pis_cofins_rate),
        "pgdas_segregated": summary.context.pgdas_segregated,
        "statuses": [finding.status.value for finding in summary.findings],
    }
    try:
        client = OpenAI(api_key=api_key.strip(), timeout=8, max_retries=0)
        response = client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "Você explica uma auditoria tributária brasileira de apoio. Não altere nem "
                        "recalcule os números fornecidos. Não prometa crédito, prazo, Pix ou deferimento. "
                        "Use linguagem condicional, fontes e validação obrigatória pelo contador."
                    ),
                },
                {"role": "user", "content": json.dumps(deterministic, ensure_ascii=False)},
            ],
            text_format=AuditOpinion,
        )
        parsed = response.output_parsed
        if parsed is None:
            return fallback
        return parsed.model_copy(update={"source": "openai"})
    except Exception:
        return fallback

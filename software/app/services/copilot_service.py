"""Copilot fiscal: respostas explicáveis, com modo local sempre disponível."""

from __future__ import annotations

from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

from app.services.openai_auditor import usable_key


SOURCES = [
    {"title": "LC 123/2006, art. 18", "url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm"},
    {"title": "Lei 10.485/2002", "url": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10485compilado.htm"},
    {"title": "Lei 10.147/2000", "url": "https://www.planalto.gov.br/ccivil_03/leis/l10147.htm"},
    {"title": "Lei 13.097/2015", "url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13097.htm"},
    {"title": "IN RFB 2.055/2021", "url": "https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=121747"},
]


class CopilotReply(BaseModel):
    answer: str
    sources: list[dict[str, str]]
    next_step: str
    source: Literal["openai", "local"] = "local"


def _local_answer(question: str) -> CopilotReply:
    normalized = question.casefold()
    if any(term in normalized for term in ("garant", "pix", "quanto tempo", "prazo")):
        answer = (
            "Não é possível garantir deferimento, pagamento ou prazo. O resultado do Audita é uma "
            "estimativa documental; a Receita pode revisar o enquadramento e exigir comprovação. "
            "O prazo prescricional em regra é analisado à luz do CTN, art. 168, mas a estratégia "
            "deve ser validada para cada período."
        )
    elif any(term in normalized for term in ("pastilha", "autope", "8708")):
        answer = (
            "A posição 87.08 consta do Anexo I da Lei 10.485/2002 e abrange desdobramentos, mas "
            "é necessário confirmar classificação, descrição, produto não usado, operação de venda "
            "e se a receita foi segregada no PGDAS-D."
        )
    elif "pgdas" in normalized or "retific" in normalized:
        answer = (
            "Primeiro reconcilie as vendas por período e valide os itens. Se a receita monofásica "
            "não foi segregada, o contador pode avaliar a retificação do PGDAS-D e o procedimento de "
            "restituição aplicável. O Audita não transmite declarações."
        )
    elif "cbs" in normalized or "2027" in normalized:
        answer = (
            "O motor precisa preservar a vigência do fato gerador: períodos legados de PIS/Cofins "
            "continuam exigindo as regras históricas, enquanto a transição para CBS a partir de 2027 "
            "demanda um catálogo próprio e acompanhamento normativo."
        )
    else:
        answer = (
            "NCM é apenas o começo. A análise combina descrição, exceções, destinação, papel do "
            "vendedor, data, CST de PIS/Cofins, CFOP de saída e segregação no PGDAS-D. Envie a "
            "pergunta com produto e período para uma resposta mais específica."
        )
    return CopilotReply(
        answer=answer,
        sources=SOURCES,
        next_step="Leve a memória e os XMLs ao contador antes de retificar ou solicitar restituição.",
        source="local",
    )


def ask_copilot(question: str, api_key: str | None = None) -> CopilotReply:
    fallback = _local_answer(question)
    if not usable_key(api_key) or any(term in question.casefold() for term in ("garant", "pix imediato")):
        return fallback
    try:
        client = OpenAI(api_key=api_key.strip(), timeout=8, max_retries=0)
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=(
                "Responda em português brasileiro como assistente tributário de apoio. Cite a lei "
                "pertinente, não prometa resultado, não invente NCM e finalize pedindo validação do contador."
            ),
            input=question[:2000],
        )
        text = (response.output_text or "").strip()
        if not text:
            return fallback
        return CopilotReply(answer=text, sources=SOURCES, next_step=fallback.next_step, source="openai")
    except Exception:
        return fallback

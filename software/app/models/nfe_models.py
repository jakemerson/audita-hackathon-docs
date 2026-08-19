"""Modelos de domínio: números fiscais permanecem em ``Decimal`` até a borda HTTP."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class AuditStatus(str, Enum):
    CONFIRMADO = "CONFIRMADO"
    REVISAR = "REVISAR"
    NAO_ENQUADRADO = "NAO_ENQUADRADO"


class Party(BaseModel):
    tax_id: str = ""
    name: str = "Não informado"
    crt: str | None = None


class NFeItem(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=False)

    line_number: int
    product_code: str = ""
    description: str
    ncm: str
    cfop: str = ""
    quantity: Decimal = Decimal("1")
    unit_value: Decimal = Decimal("0")
    product_value: Decimal
    pis_cst: str | None = None
    cofins_cst: str | None = None
    icms_cst: str | None = None
    csosn: str | None = None

    @property
    def is_sale(self) -> bool:
        """CFOP 5/6/7 representa saída; compra (1/2/3) não constitui receita."""
        return bool(self.cfop) and self.cfop[0] in {"5", "6", "7"}


class NFeDocument(BaseModel):
    access_key: str = ""
    number: str
    series: str = ""
    issued_at: datetime | None = None
    model: str = "55"
    issuer: Party
    recipient: Party
    items: list[NFeItem] = Field(default_factory=list)
    synthetic_fixture: bool = False

    @property
    def total_products(self) -> Decimal:
        return sum((item.product_value for item in self.items), Decimal("0"))


class AuditContext(BaseModel):
    rbt12: Decimal = Field(gt=0, le=Decimal("3600000"))
    annex: str = "I"
    pgdas_segregated: bool = False
    period: str = "2026-08"


class RateBreakdown(BaseModel):
    band: int
    nominal_rate: Decimal
    deduction: Decimal
    effective_das_rate: Decimal
    pis_cofins_share: Decimal
    effective_pis_cofins_rate: Decimal


class RuleEvidence(BaseModel):
    rule_id: str
    legal_source: str
    legal_url: str
    valid_from: str
    valid_to: str | None = None
    match_type: str
    reason: str
    caveats: list[str] = Field(default_factory=list)


class AuditFinding(BaseModel):
    invoice_number: str
    item_number: int
    product_code: str
    description: str
    ncm: str
    cfop: str
    product_value: Decimal
    pis_cst: str | None = None
    cofins_cst: str | None = None
    csosn: str | None = None
    status: AuditStatus
    segment: str
    signal: str
    estimated_overpayment: Decimal = Decimal("0")
    evidence: RuleEvidence | None = None
    pending_checks: list[str] = Field(default_factory=list)


class AuditSummary(BaseModel):
    context: AuditContext
    rate: RateBreakdown
    invoice_count: int
    item_count: int
    audited_revenue: Decimal
    confirmed_monophase_revenue: Decimal
    review_revenue: Decimal
    estimated_overpayment: Decimal
    findings: list[AuditFinding]
    warnings: list[str]
    synthetic_simulation: bool = False

    def public_dict(self) -> dict:
        """JSON compatível sem perder a exatidão decimal no domínio."""
        return self.model_dump(mode="json")


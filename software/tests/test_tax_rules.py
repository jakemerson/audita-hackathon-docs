from decimal import Decimal

import pytest

from app.core.tax_rules import calculate_annex_i_rate, classify_item
from app.models.nfe_models import AuditContext, AuditStatus, NFeItem


def test_first_annex_band_is_four_percent():
    rate = calculate_annex_i_rate("180000")
    assert rate.band == 1
    assert rate.effective_das_rate == Decimal("0.04")
    assert rate.effective_pis_cofins_rate == Decimal("0.00620")


def test_fourth_band_calculation_is_formula_based():
    rate = calculate_annex_i_rate("1800000")
    assert rate.band == 4
    assert rate.effective_das_rate == Decimal("0.0945")
    assert rate.effective_pis_cofins_rate == Decimal("0.0146475")


@pytest.mark.parametrize("invalid", ["0", "-1", "3600000.01"])
def test_annex_rate_rejects_unsupported_revenue(invalid):
    with pytest.raises(ValueError):
        calculate_annex_i_rate(invalid)


def test_confirmed_auto_part_has_explainable_estimate(context, sale_item):
    finding = classify_item(sale_item, "1001", context)
    assert finding.status == AuditStatus.CONFIRMADO
    assert finding.estimated_overpayment == Decimal("14.65")
    assert finding.evidence.rule_id == "AUTO-8708"


def test_pgdas_segregation_zeros_potential(sale_item):
    context = AuditContext(rbt12=Decimal("1800000"), pgdas_segregated=True)
    finding = classify_item(sale_item, "1001", context)
    assert finding.status == AuditStatus.CONFIRMADO
    assert finding.estimated_overpayment == 0


def test_purchase_xml_is_not_treated_as_proven_revenue(context, sale_item):
    purchase = sale_item.model_copy(update={"cfop": "1102"})
    finding = classify_item(purchase, "1001", context)
    assert finding.status == AuditStatus.REVISAR
    assert finding.estimated_overpayment == 0
    assert "compra isolado" in finding.pending_checks[0]


def test_csosn_is_explicitly_kept_out_of_pis_decision(context, sale_item):
    finding = classify_item(sale_item, "1001", context)
    assert any("pertence ao ICMS" in text for text in finding.pending_checks)
    assert "PIS/Cofins" in finding.signal


def test_used_tyre_is_excluded(context, sale_item):
    tyre = sale_item.model_copy(update={"ncm": "40111000", "description": "Pneu usado"})
    finding = classify_item(tyre, "1001", context)
    assert finding.status == AuditStatus.NAO_ENQUADRADO
    assert finding.estimated_overpayment == 0


def test_ambiguous_drink_requires_description(context, sale_item):
    drink = sale_item.model_copy(update={"ncm": "22029900", "description": "Bebida composta"})
    finding = classify_item(drink, "1001", context)
    assert finding.status == AuditStatus.REVISAR
    assert finding.estimated_overpayment == 0

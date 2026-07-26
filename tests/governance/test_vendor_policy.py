from decimal import Decimal

from cancion.common import ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.governance.context import EvaluationContext, SpendRequest
from cancion.governance.policies.vendor import VendorRule
from cancion.governance.rule_result import RuleOutcome


def make_context(vendor: str) -> EvaluationContext:
    contract = Contract(
        vendor="Netflix",
        action="renew",
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
    )

    request = SpendRequest(
        vendor=vendor,
        action="renew",
        amount=Money(Decimal("18")),
    )

    return EvaluationContext(
        contract=contract,
        request=request,
    )


def test_vendor_matches() -> None:
    result = VendorRule().evaluate(make_context("Netflix"))

    assert result.outcome is RuleOutcome.PASS
    assert result.reason is None


def test_vendor_mismatch() -> None:
    result = VendorRule().evaluate(make_context("Spotify"))

    assert result.outcome is RuleOutcome.FAIL
    assert result.reason is not None
    assert "Vendor mismatch" in result.reason

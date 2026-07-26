from decimal import Decimal

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.governance.context import EvaluationContext, SpendRequest
from cancion.governance.policies.amount import AmountRule
from cancion.governance.rule_result import RuleOutcome


def make_context(amount: str) -> EvaluationContext:
    contract = Contract(
        vendor="Netflix",
        action=Action.RENEW,
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
    )

    request = SpendRequest(
        vendor="Netflix",
        action="renew",
        amount=Money(Decimal(amount)),
    )

    return EvaluationContext(
        contract=contract,
        request=request,
    )


def test_amount_within_limit() -> None:
    result = AmountRule().evaluate(make_context("16"))

    assert result.outcome is RuleOutcome.PASS
    assert result.reason is None


def test_amount_exceeds_limit() -> None:
    result = AmountRule().evaluate(make_context("25"))

    assert result.outcome is RuleOutcome.FAIL
    assert result.reason is not None
    assert "Amount exceeds policy" in result.reason

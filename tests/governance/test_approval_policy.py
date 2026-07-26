from decimal import Decimal

from cancion.common import (
    Action,
    ApprovalMode,
    Frequency,
)
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.governance.context import (
    EvaluationContext,
    SpendRequest,
)
from cancion.governance.policies.approval import ApprovalRule
from cancion.governance.rule_result import RuleOutcome


def make_context(mode: ApprovalMode) -> EvaluationContext:
    contract = Contract(
        vendor="Netflix",
        action=Action.RENEW,
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=mode,
    )

    request = SpendRequest(
        vendor="Netflix",
        action=Action.RENEW,
        amount=Money(Decimal("18")),
    )

    return EvaluationContext(
        contract=contract,
        request=request,
    )


def test_auto_approval_passes() -> None:
    result = ApprovalRule().evaluate(make_context(ApprovalMode.AUTO))

    assert result.outcome is RuleOutcome.PASS
    assert result.reason is None


def test_manual_approval_escalates() -> None:
    result = ApprovalRule().evaluate(make_context(ApprovalMode.MANUAL))

    assert result.outcome is RuleOutcome.ESCALATE
    assert result.reason == "Manual approval required."

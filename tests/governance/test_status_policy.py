from decimal import Decimal

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract, ContractStatus
from cancion.governance.context import EvaluationContext, SpendRequest
from cancion.governance.policies.status import StatusRule
from cancion.governance.rule_result import RuleOutcome


def make_context(status: ContractStatus) -> EvaluationContext:
    contract = Contract(
        vendor="Netflix",
        action=Action.RENEW,
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
        status=status,
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


def test_active_contract() -> None:
    result = StatusRule().evaluate(make_context(ContractStatus.ACTIVE))

    assert result.outcome is RuleOutcome.PASS
    assert result.reason is None


def test_revoked_contract() -> None:
    result = StatusRule().evaluate(make_context(ContractStatus.REVOKED))

    assert result.outcome is RuleOutcome.FAIL
    assert result.reason is not None
    assert "revoked" in result.reason.lower()

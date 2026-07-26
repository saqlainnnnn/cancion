from decimal import Decimal

from cancion.common import ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.domain.decision import DecisionOutcome
from cancion.governance.context import EvaluationContext, SpendRequest
from cancion.governance.engine import GovernanceEngine
from cancion.governance.rules import Rule, RuleResult


class PassRule(Rule):
    def evaluate(self, context: EvaluationContext) -> str | None:
        return RuleResult.passed()


class FailRule(Rule):
    def evaluate(self, context: EvaluationContext) -> str | None:
        return RuleResult.failed("failed")


class EscalateRule(Rule):
    def evaluate(
        self,
        context: EvaluationContext,
    ) -> RuleResult:
        return RuleResult.escalated("Manual approval required.")


def make_context() -> EvaluationContext:
    contract = Contract(
        vendor="Netflix",
        action="renew",
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
    )

    request = SpendRequest(
        vendor="Netflix",
        action="renew",
        amount=Money(Decimal("18")),
    )

    return EvaluationContext(
        contract=contract,
        request=request,
    )


def test_escalation_returns_escalate() -> None:
    engine = GovernanceEngine(
        [
            PassRule(),
            EscalateRule(),
            PassRule(),
        ]
    )

    decision = engine.evaluate(make_context())

    assert decision.outcome is DecisionOutcome.ESCALATE
    assert decision.reasons == ["Manual approval required."]


def test_all_rules_pass() -> None:
    engine = GovernanceEngine([PassRule(), PassRule()])

    decision = engine.evaluate(make_context())

    assert decision.outcome == DecisionOutcome.APPROVE
    assert decision.reasons == []


def test_any_rule_failure_denies() -> None:
    engine = GovernanceEngine(
        [
            PassRule(),
            FailRule(),
            PassRule(),
        ]
    )

    decision = engine.evaluate(make_context())

    assert decision.outcome == DecisionOutcome.DENY
    assert decision.reasons == ["failed"]


def test_failure_takes_precedence_over_escalation() -> None:
    engine = GovernanceEngine(
        [
            PassRule(),
            EscalateRule(),
            FailRule(),
        ]
    )

    decision = engine.evaluate(make_context())

    assert decision.outcome is DecisionOutcome.DENY

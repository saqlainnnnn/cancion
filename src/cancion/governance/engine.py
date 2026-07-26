from collections.abc import Iterable

from cancion.domain.decision import Decision, DecisionOutcome
from cancion.governance.context import EvaluationContext
from cancion.governance.rule_result import RuleOutcome
from cancion.governance.rules import Rule


class GovernanceEngine:
    """Evaluates a spend request against a sequence of governance rules."""

    def __init__(self, rules: Iterable[Rule]) -> None:
        self._rules = tuple(rules)

    def evaluate(self, context: EvaluationContext) -> Decision:
        failures: list[str] = []
        escalations: list[str] = []

        for rule in self._rules:
            result = rule.evaluate(context)

            if result.outcome is RuleOutcome.FAIL:
                if result.reason is not None:
                    failures.append(result.reason)
            elif result.outcome is RuleOutcome.ESCALATE and result.reason is not None:
                escalations.append(result.reason)

        if failures:
            return Decision(
                outcome=DecisionOutcome.DENY,
                reasons=failures,
            )

        if escalations:
            return Decision(
                outcome=DecisionOutcome.ESCALATE,
                reasons=escalations,
            )

        return Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=[],
        )

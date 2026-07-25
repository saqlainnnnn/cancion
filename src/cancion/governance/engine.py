from cancion.domain.decision import Decision, DecisionOutcome
from cancion.governance.context import EvaluationContext
from cancion.governance.rules import Rule


class GovernanceEngine:
    """Evaluates spend requests against governance rules."""

    def __init__(self, rules: list[Rule]) -> None:
        self._rules = rules

    def evaluate(self, context: EvaluationContext) -> Decision:
        reasons: list[str] = []

        for rule in self._rules:
            result = rule.evaluate(context)

            if result is not None:
                reasons.append(result)

        if reasons:
            return Decision(
                outcome=DecisionOutcome.DENY,
                reasons=reasons,
            )

        return Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=[],
        )

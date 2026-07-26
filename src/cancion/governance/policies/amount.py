from cancion.governance.context import EvaluationContext
from cancion.governance.rule_result import RuleResult
from cancion.governance.rules import Rule


class AmountRule(Rule):
    """Ensures the requested amount does not exceed the contract limit."""

    def evaluate(self, context: EvaluationContext) -> RuleResult:
        if context.request.amount.amount > context.contract.max_amount.amount:
            return RuleResult.failed(
                f"Amount exceeds policy: {context.request.amount} > {context.contract.max_amount}."
            )

        return RuleResult.passed()

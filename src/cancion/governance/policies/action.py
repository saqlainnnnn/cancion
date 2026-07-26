from cancion.governance.context import EvaluationContext
from cancion.governance.rules import Rule


class ActionRule(Rule):
    """Ensures the requested action matches the contract."""

    def evaluate(self, context: EvaluationContext) -> str | None:
        if context.request.action != context.contract.action:
            return (
                f"Action mismatch: expected "
                f"{context.contract.action.value}, "
                f"got {context.request.action.value}."
            )

        return None

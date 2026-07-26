from cancion.domain.contract import ContractStatus
from cancion.governance.context import EvaluationContext
from cancion.governance.rules import Rule


class StatusRule(Rule):
    """Ensures the contract is active."""

    def evaluate(self, context: EvaluationContext) -> str | None:
        if context.contract.status is not ContractStatus.ACTIVE:
            return f"Contract is {context.contract.status.value}."

        return None

from cancion.domain.contract import ContractStatus
from cancion.governance.context import EvaluationContext
from cancion.governance.rule_result import RuleResult
from cancion.governance.rules import Rule


class StatusRule(Rule):
    """Ensures the contract is active."""

    def evaluate(self, context: EvaluationContext) -> RuleResult:
        if context.contract.status is not ContractStatus.ACTIVE:
            return RuleResult.failed(f"Contract is {context.contract.status.value}.")

        return RuleResult.passed()

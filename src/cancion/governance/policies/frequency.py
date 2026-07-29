from cancion.governance.context import EvaluationContext
from cancion.governance.rule_result import RuleResult
from cancion.governance.rules import Rule
from cancion.services.spend_ledger import SpendLedgerService


class FrequencyRule(Rule):
    """Ensures cumulative spend does not exceed the contract budget."""

    def __init__(
        self,
        ledger_service: SpendLedgerService,
    ) -> None:
        self._ledger_service = ledger_service

    def evaluate(
        self,
        context: EvaluationContext,
    ) -> RuleResult:
        ledger = self._ledger_service.current(
            contract=context.contract,
        )

        projected = ledger.spent_amount + context.request.amount

        if projected > context.contract.max_amount:
            return RuleResult.failed(
                f"Cumulative spend exceeds policy: {projected} > {context.contract.max_amount}."
            )

        return RuleResult.passed()

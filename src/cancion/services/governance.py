from cancion.domain.contract import Contract
from cancion.domain.decision import Decision
from cancion.governance.context import (
    EvaluationContext,
    SpendRequest,
)
from cancion.governance.engine import GovernanceEngine
from cancion.governance.policies.action import ActionRule
from cancion.governance.policies.amount import AmountRule
from cancion.governance.policies.approval import ApprovalRule
from cancion.governance.policies.status import StatusRule
from cancion.governance.policies.vendor import VendorRule


class GovernanceService:
    """Evaluates spend requests against governance policies."""

    def __init__(self) -> None:
        self._engine = GovernanceEngine(
            [
                VendorRule(),
                ActionRule(),
                AmountRule(),
                StatusRule(),
                ApprovalRule(),
            ]
        )

    def evaluate(
        self,
        contract: Contract,
        request: SpendRequest,
    ) -> Decision:
        context = EvaluationContext(
            contract=contract,
            request=request,
        )

        return self._engine.evaluate(context)

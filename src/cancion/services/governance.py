from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from cancion.domain.contract import Contract
from cancion.domain.decision import (
    Decision,
    DecisionOutcome,
)
from cancion.domain.decision_record import DecisionRecord
from cancion.governance.context import (
    EvaluationContext,
    SpendRequest,
)
from cancion.governance.engine import GovernanceEngine
from cancion.repositories.decision import DecisionRepository
from cancion.services.spend_ledger import SpendLedgerService


class GovernanceService:
    """Evaluates spend requests against governance policies."""

    def __init__(
        self,
        engine: GovernanceEngine,
        repository: DecisionRepository,
        ledger_service: SpendLedgerService,
    ) -> None:
        self._engine = engine
        self._repository = repository
        self._ledger_service = ledger_service

    def evaluate(
        self,
        contract: Contract,
        request: SpendRequest,
    ) -> Decision:
        context = EvaluationContext(
            contract=contract,
            request=request,
        )

        decision = self._engine.evaluate(context)

        record = DecisionRecord(
            id=uuid4(),
            contract_id=contract.id,
            vendor=request.vendor,
            action=request.action,
            amount=request.amount,
            decision=decision,
            created_at=datetime.now(UTC),
        )

        self._repository.save(record)

        if decision.outcome is DecisionOutcome.APPROVE:
            self._ledger_service.record_spend(
                contract=contract,
                amount=request.amount,
            )

        return decision

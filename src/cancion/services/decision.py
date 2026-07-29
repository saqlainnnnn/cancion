from __future__ import annotations

from uuid import UUID

from cancion.domain.decision_record import DecisionRecord
from cancion.repositories.decision import DecisionRepository


class DecisionService:
    """Application service for decision records."""

    def __init__(
        self,
        repository: DecisionRepository,
    ) -> None:
        self._repository = repository

    def get(
        self,
        decision_id: UUID,
    ) -> DecisionRecord | None:
        return self._repository.get(decision_id)

    def list(self) -> list[DecisionRecord]:
        return self._repository.list_all()

    def list_by_contract(
        self,
        contract_id: UUID,
    ) -> list[DecisionRecord]:
        return self._repository.list_by_contract(contract_id)

    def delete(
        self,
        decision_id: UUID,
    ) -> bool:
        return self._repository.delete(decision_id)

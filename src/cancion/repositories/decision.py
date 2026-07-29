from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from cancion.db.mappers.decision import (
    to_domain,
    to_model,
)
from cancion.db.models.decision import DecisionModel
from cancion.domain.decision_record import DecisionRecord


class DecisionRepository:
    """Repository for DecisionRecord persistence."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        record: DecisionRecord,
    ) -> DecisionRecord:
        model = to_model(record)

        self._session.merge(model)
        self._session.commit()

        return record

    def get(
        self,
        decision_id: UUID,
    ) -> DecisionRecord | None:
        model = self._session.get(
            DecisionModel,
            decision_id,
        )

        if model is None:
            return None

        return to_domain(model)

    def list_all(
        self,
    ) -> list[DecisionRecord]:
        models = self._session.scalars(
            select(DecisionModel),
        ).all()

        return [to_domain(model) for model in models]

    def list_by_contract(
        self,
        contract_id: UUID,
    ) -> list[DecisionRecord]:
        models = self._session.scalars(
            select(DecisionModel).where(
                DecisionModel.contract_id == contract_id,
            ),
        ).all()

        return [to_domain(model) for model in models]

    def delete(
        self,
        decision_id: UUID,
    ) -> bool:
        model = self._session.get(
            DecisionModel,
            decision_id,
        )

        if model is None:
            return False

        self._session.delete(model)
        self._session.commit()

        return True

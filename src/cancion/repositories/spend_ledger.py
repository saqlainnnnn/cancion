from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from cancion.db.mappers.spend_ledger import to_domain, to_model
from cancion.db.models.spend_ledger import SpendLedgerModel
from cancion.domain.spend_ledger import SpendLedger


class SpendLedgerRepository:
    """Repository for SpendLedger persistence."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, ledger: SpendLedger) -> SpendLedger:
        model = to_model(ledger)

        self._session.merge(model)
        self._session.commit()

        return ledger

    def get(self, ledger_id: UUID) -> SpendLedger | None:
        model = self._session.get(
            SpendLedgerModel,
            ledger_id,
        )

        if model is None:
            return None

        return to_domain(model)

    def get_active(
        self,
        contract_id: UUID,
        at: datetime | None = None,
    ) -> SpendLedger | None:
        """Return the ledger whose period contains the supplied timestamp."""

        if at is None:
            at = datetime.now(UTC)

        model = self._session.scalar(
            select(SpendLedgerModel).where(
                and_(
                    SpendLedgerModel.contract_id == contract_id,
                    SpendLedgerModel.period_start <= at,
                    SpendLedgerModel.period_end > at,
                )
            )
        )

        if model is None:
            return None

        return to_domain(model)

    def list_for_contract(
        self,
        contract_id: UUID,
    ) -> list[SpendLedger]:
        models = self._session.scalars(
            select(SpendLedgerModel)
            .where(SpendLedgerModel.contract_id == contract_id)
            .order_by(SpendLedgerModel.period_start.desc())
        ).all()

        return [to_domain(model) for model in models]

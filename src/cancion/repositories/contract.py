from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from cancion.db.mappers.contract import to_domain, to_model
from cancion.db.models.contract import ContractModel
from cancion.domain.contract import Contract


class ContractRepository:
    """Repository for Contract persistence."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, contract: Contract) -> Contract:
        model = to_model(contract)

        self._session.merge(model)
        self._session.commit()

        return contract

    def get(self, contract_id: UUID) -> Contract | None:
        model = self._session.get(
            ContractModel,
            contract_id,
        )

        if model is None:
            return None

        return to_domain(model)

    def list(self) -> list[Contract]:
        models = self._session.scalars(select(ContractModel)).all()

        return [to_domain(model) for model in models]

    def delete(
        self,
        contract_id: UUID,
    ) -> bool:
        model = self._session.get(
            ContractModel,
            contract_id,
        )

        if model is None:
            return False

        self._session.delete(model)
        self._session.commit()

        return True

from uuid import UUID

from cancion.domain.contract import Contract
from cancion.domain.factory import ContractFactory
from cancion.domain.intent import Intent
from cancion.domain.update_contract import UpdateContract
from cancion.repositories.contract import ContractRepository


class ContractService:
    def __init__(
        self,
        repository: ContractRepository,
        factory: ContractFactory,
    ) -> None:
        self._repository = repository
        self._factory = factory

    def create(self, intent: Intent) -> Contract:
        contract = self._factory.create(intent)
        self._repository.save(contract)
        return contract

    def get(self, contract_id: UUID) -> Contract | None:
        return self._repository.get(contract_id)

    def list(self) -> list[Contract]:
        return self._repository.list()

    def list_inactive(self) -> list[Contract]:
        return self._repository.list_inactive()

    def update(
        self,
        contract_id: UUID,
        update: UpdateContract,
    ) -> Contract | None:
        contract = self._repository.get(contract_id)

        if contract is None:
            return None

        updated = contract.update(
            vendor=update.vendor,
            action=update.action,
            max_amount=update.max_amount,
            frequency=update.frequency,
            approval_mode=update.approval_mode,
        )

        self._repository.save(updated)

        return updated

    def delete(self, contract_id: UUID) -> bool:
        return self._repository.delete(contract_id)

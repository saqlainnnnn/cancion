from uuid import UUID

from cancion.domain.contract import Contract
from cancion.domain.factory import ContractFactory
from cancion.domain.intent import Intent
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

    def delete(self, contract_id: UUID) -> bool:
        return self._repository.delete(contract_id)

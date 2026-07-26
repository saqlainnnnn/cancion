from decimal import Decimal

from cancion.common.enums import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.factory import ContractFactory
from cancion.domain.intent import Intent
from cancion.repositories.contract import ContractRepository
from cancion.services.contract import ContractService


def make_intent(
    vendor: str = "Netflix",
    action: Action = Action.RENEW,
    amount: Decimal = Decimal("18.00"),
    frequency: Frequency = Frequency.MONTHLY,
    approval_mode: ApprovalMode = ApprovalMode.AUTO,
) -> Intent:
    return Intent(
        vendor=vendor,
        action=action,
        max_amount=Money(amount),
        frequency=frequency,
        approval_mode=approval_mode,
    )


def make_service(session):
    repository = ContractRepository(session)
    factory = ContractFactory()
    return ContractService(repository, factory)


def test_create_contract(session):
    service = make_service(session)

    contract = service.create(make_intent())

    assert contract.vendor == "Netflix"
    assert service.get(contract.id) == contract


def test_get_contract(session):
    service = make_service(session)

    created = service.create(make_intent())

    loaded = service.get(created.id)

    assert loaded == created


def test_list_contracts(session):
    service = make_service(session)

    service.create(make_intent(vendor="Netflix"))
    service.create(make_intent(vendor="Spotify"))

    contracts = service.list()

    assert len(contracts) == 2


def test_delete_contract(session):
    service = make_service(session)

    contract = service.create(make_intent())

    assert service.delete(contract.id)
    assert service.get(contract.id) is None

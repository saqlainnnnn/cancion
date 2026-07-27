from decimal import Decimal

from cancion.api.mappers.contract import to_contract_response
from cancion.common import Action, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract


def test_to_contract_response_maps_domain_model():
    contract = Contract(
        vendor="Amazon",
        action=Action.PAY,
        max_amount=Money(Decimal("100.00")),
        frequency=Frequency.MONTHLY,
    )

    response = to_contract_response(contract)

    assert response.id == contract.id
    assert response.vendor == contract.vendor
    assert response.action == contract.action

    assert response.max_amount.amount == Decimal("100.00")
    assert response.max_amount.currency == "USD"

    assert response.frequency == contract.frequency
    assert response.approval_mode == contract.approval_mode
    assert response.status == contract.status
    assert response.version == contract.version
    assert response.agent_id == contract.agent_id
    assert response.created_at == contract.created_at
    assert response.updated_at == contract.updated_at

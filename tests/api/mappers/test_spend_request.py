from decimal import Decimal
from uuid import uuid4

from cancion.api.mappers.spend_request import (
    to_spend_request,
)
from cancion.api.schemas.common import MoneyRequest
from cancion.api.schemas.evaluation import (
    SpendRequestSchema,
)
from cancion.common import Action


def test_to_spend_request():
    request = SpendRequestSchema(
        contract_id=uuid4(),
        vendor="Amazon",
        action=Action.PAY,
        amount=MoneyRequest(
            amount=Decimal("50.00"),
            currency="USD",
        ),
    )

    spend_request = to_spend_request(request)

    assert spend_request.vendor == "Amazon"
    assert spend_request.action.value == "pay"
    assert spend_request.amount.amount == Decimal("50.00")
    assert spend_request.amount.currency == "USD"

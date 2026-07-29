from cancion.api.schemas.evaluation import SpendRequestSchema
from cancion.common.money import Money
from cancion.governance.context import SpendRequest


def to_spend_request(
    request: SpendRequestSchema,
) -> SpendRequest:
    """Convert an API request into a domain spend request."""

    return SpendRequest(
        vendor=request.vendor,
        action=request.action,
        amount=Money(
            amount=request.amount.amount,
            currency=request.amount.currency,
        ),
    )

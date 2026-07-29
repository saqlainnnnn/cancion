from cancion.api.schemas.common import MoneyResponse
from cancion.api.schemas.decision import DecisionResponse
from cancion.domain.decision_record import DecisionRecord


def to_decision_response(
    decision: DecisionRecord,
) -> DecisionResponse:
    """Convert a domain DecisionRecord into an API response."""

    return DecisionResponse(
        id=decision.id,
        contract_id=decision.contract_id,
        vendor=decision.vendor,
        action=decision.action,
        amount=MoneyResponse(
            amount=decision.amount.amount,
            currency=decision.amount.currency,
        ),
        outcome=decision.decision.outcome,
        reasons=decision.decision.reasons,
        created_at=decision.created_at,
    )

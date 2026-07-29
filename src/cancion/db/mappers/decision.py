from datetime import UTC
from decimal import Decimal

from cancion.common.money import Money
from cancion.db.models.decision import DecisionModel
from cancion.domain.decision import (
    Decision,
    DecisionOutcome,
)
from cancion.domain.decision_record import DecisionRecord


def to_model(
    record: DecisionRecord,
) -> DecisionModel:
    """Convert a domain decision record to a database model."""
    return DecisionModel(
        id=record.id,
        contract_id=record.contract_id,
        vendor=record.vendor,
        action=record.action,
        amount=str(record.amount.amount),
        currency=record.amount.currency,
        outcome=record.decision.outcome,
        reasons=record.decision.reasons,
        created_at=record.created_at,
    )


def to_domain(
    model: DecisionModel,
) -> DecisionRecord:
    """Convert a database model to a domain decision record."""
    return DecisionRecord(
        id=model.id,
        contract_id=model.contract_id,
        vendor=model.vendor,
        action=model.action,
        amount=Money(
            amount=Decimal(model.amount),
            currency=model.currency,
        ),
        decision=Decision(
            outcome=DecisionOutcome(model.outcome),
            reasons=model.reasons,
        ),
        created_at=model.created_at.replace(tzinfo=UTC),
    )

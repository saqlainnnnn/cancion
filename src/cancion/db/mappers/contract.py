from datetime import UTC, datetime
from decimal import Decimal

from cancion.common.money import Money
from cancion.db.models.contract import ContractModel
from cancion.domain.contract import Contract


def to_model(contract: Contract) -> ContractModel:
    return ContractModel(
        id=contract.id,
        vendor=contract.vendor,
        action=contract.action,
        max_amount=contract.max_amount.amount,
        frequency=contract.frequency,
        approval_mode=contract.approval_mode,
        status=contract.status,
        version=contract.version,
        agent_id=contract.agent_id,
        created_at=contract.created_at,
        updated_at=contract.updated_at,
    )


def to_domain(model: ContractModel) -> Contract:
    return Contract(
        id=model.id,
        vendor=model.vendor,
        action=model.action,
        max_amount=Money(Decimal(model.max_amount)),
        frequency=model.frequency,
        approval_mode=model.approval_mode,
        status=model.status,
        version=model.version,
        agent_id=model.agent_id,
        created_at=_normalize_datetime(model.created_at),
        updated_at=_normalize_datetime(model.updated_at),
    )


def _normalize_datetime(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)

    return dt.astimezone(UTC)

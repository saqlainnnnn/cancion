from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from cancion.common import Action
from cancion.common.money import Money
from cancion.domain.decision import Decision


@dataclass(slots=True)
class DecisionRecord:
    """A persisted governance evaluation."""

    id: UUID
    contract_id: UUID

    vendor: str
    action: Action
    amount: Money

    decision: Decision

    created_at: datetime

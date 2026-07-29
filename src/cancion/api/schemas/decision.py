from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from cancion.common import Action
from cancion.domain.decision import DecisionOutcome

from .common import MoneyResponse


class DecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    contract_id: UUID

    vendor: str
    action: Action

    amount: MoneyResponse

    outcome: DecisionOutcome
    reasons: list[str]

    created_at: datetime

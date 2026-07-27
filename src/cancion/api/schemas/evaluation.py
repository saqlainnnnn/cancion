from uuid import UUID

from pydantic import BaseModel

from cancion.common import Action

from .common import MoneyResponse


class SpendRequestSchema(BaseModel):
    contract_id: UUID
    vendor: str
    action: Action
    amount: MoneyResponse


class EvaluationResponse(BaseModel):
    outcome: str
    reasons: list[str]

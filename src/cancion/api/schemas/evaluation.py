from uuid import UUID

from pydantic import BaseModel

from cancion.common import Action

from .common import MoneyRequest


class SpendRequestSchema(BaseModel):
    contract_id: UUID
    vendor: str
    action: Action
    amount: MoneyRequest


class EvaluationResponse(BaseModel):
    outcome: str
    reasons: list[str]

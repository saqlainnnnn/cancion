from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from cancion.common import Action, ApprovalMode, Frequency
from cancion.domain.contract import ContractStatus

from .common import MoneyResponse


class CreateContractRequest(BaseModel):
    text: str


class ContractResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    vendor: str
    action: Action

    max_amount: MoneyResponse
    frequency: Frequency

    approval_mode: ApprovalMode
    status: ContractStatus

    version: int
    agent_id: UUID | None

    created_at: datetime
    updated_at: datetime

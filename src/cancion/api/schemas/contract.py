from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateContractRequest(BaseModel):
    text: str


class ContractResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    merchant: str
    category: str
    limit: float
    currency: str
    period: str

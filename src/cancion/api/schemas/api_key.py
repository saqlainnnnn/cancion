from uuid import UUID

from pydantic import BaseModel

from cancion.domain.api_key import ApiKeyStatus


class CreateApiKeyRequest(BaseModel):
    agent_id: UUID
    name: str
    key_hash: str


class UpdateApiKeyRequest(BaseModel):
    name: str
    key_hash: str


class ApiKeyResponse(BaseModel):
    id: UUID
    agent_id: UUID
    name: str
    key_hash: str
    status: ApiKeyStatus

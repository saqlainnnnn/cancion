from uuid import UUID

from pydantic import BaseModel

from cancion.domain.agent import AgentStatus


class CreateAgentRequest(BaseModel):
    organization_id: UUID
    name: str
    description: str | None = None


class UpdateAgentRequest(BaseModel):
    name: str
    description: str | None = None


class AgentResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    description: str | None
    status: AgentStatus

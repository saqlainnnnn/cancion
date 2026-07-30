from uuid import UUID

from pydantic import BaseModel

from cancion.domain.organization import OrganizationStatus


class CreateOrganizationRequest(BaseModel):
    name: str
    slug: str


class UpdateOrganizationRequest(BaseModel):
    name: str
    slug: str


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    status: OrganizationStatus

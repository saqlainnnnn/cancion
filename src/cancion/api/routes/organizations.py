from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from cancion.api.dependencies import get_organization_service
from cancion.api.schemas.organization import (
    CreateOrganizationRequest,
    OrganizationResponse,
    UpdateOrganizationRequest,
)
from cancion.db.mappers.organization import to_organization_response
from cancion.domain.organization import Organization
from cancion.services.organization import OrganizationService

router = APIRouter()


@router.get("/", response_model=list[OrganizationResponse])
def list_organizations(
    service: OrganizationService = Depends(get_organization_service),
):
    return [to_organization_response(org) for org in service.list()]


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    organization = service.get(organization_id)

    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    return to_organization_response(organization)


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    request: CreateOrganizationRequest,
    service: OrganizationService = Depends(get_organization_service),
):
    organization = Organization(
        name=request.name,
        slug=request.slug,
    )

    return to_organization_response(service.create(organization))


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def update_organization(
    organization_id: UUID,
    request: UpdateOrganizationRequest,
    service: OrganizationService = Depends(get_organization_service),
):
    organization = service.get(organization_id)

    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    updated = Organization(
        id=organization.id,
        name=request.name,
        slug=request.slug,
        status=organization.status,
        created_at=organization.created_at,
        updated_at=organization.updated_at,
    )

    return to_organization_response(service.update(updated))


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    deleted = service.delete(organization_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

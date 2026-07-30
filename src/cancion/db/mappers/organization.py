from datetime import UTC, datetime

from cancion.api.schemas.organization import OrganizationResponse
from cancion.db.models.organization import OrganizationModel
from cancion.domain.organization import Organization


def to_model(organization: Organization) -> OrganizationModel:
    return OrganizationModel(
        id=organization.id,
        name=organization.name,
        slug=organization.slug,
        status=organization.status,
        created_at=organization.created_at,
        updated_at=organization.updated_at,
    )


def to_domain(model: OrganizationModel) -> Organization:
    return Organization(
        id=model.id,
        name=model.name,
        slug=model.slug,
        status=model.status,
        created_at=_normalize_datetime(model.created_at),
        updated_at=_normalize_datetime(model.updated_at),
    )


def _normalize_datetime(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)

    return dt.astimezone(UTC)


def to_organization_response(organization: Organization) -> OrganizationResponse:
    return OrganizationResponse(
        id=organization.id,
        name=organization.name,
        slug=organization.slug,
        status=organization.status,
    )

from uuid import UUID

from cancion.domain.organization import Organization
from cancion.repositories.organization import OrganizationRepository


class OrganizationService:
    """Application service for organizations."""

    def __init__(
        self,
        repository: OrganizationRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        organization: Organization,
    ) -> Organization:
        self._repository.save(organization)

        return organization

    def get(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        return self._repository.get(organization_id)

    def list(self) -> list[Organization]:
        return self._repository.list()

    def update(
        self,
        organization: Organization,
    ) -> Organization:
        self._repository.save(organization)

        return organization

    def delete(
        self,
        organization_id: UUID,
    ) -> bool:
        return self._repository.delete(organization_id)

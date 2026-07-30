from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from cancion.db.mappers.organization import to_domain, to_model
from cancion.db.models.organization import OrganizationModel
from cancion.domain.organization import Organization


class OrganizationRepository:
    """Repository for Organization persistence."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, organization: Organization) -> Organization:
        model = to_model(organization)

        self._session.merge(model)
        self._session.commit()

        return organization

    def get(self, organization_id: UUID) -> Organization | None:
        model = self._session.get(
            OrganizationModel,
            organization_id,
        )

        if model is None:
            return None

        return to_domain(model)

    def list(self) -> list[Organization]:
        models = self._session.scalars(select(OrganizationModel)).all()

        return [to_domain(model) for model in models]

    def delete(
        self,
        organization_id: UUID,
    ) -> bool:
        model = self._session.get(
            OrganizationModel,
            organization_id,
        )

        if model is None:
            return False

        self._session.delete(model)
        self._session.commit()

        return True

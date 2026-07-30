from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from cancion.db.mappers.api_key import (
    to_domain,
    to_model,
)
from cancion.db.models.api_key import ApiKeyModel
from cancion.domain.api_key import ApiKey


class ApiKeyRepository:
    """Repository for API key entities."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        api_key: ApiKey,
    ) -> ApiKey:
        model = to_model(api_key)

        model = self._session.merge(model)

        self._session.commit()

        return to_domain(model)

    def get(
        self,
        api_key_id: UUID,
    ) -> ApiKey | None:
        model = self._session.get(
            ApiKeyModel,
            api_key_id,
        )

        if model is None:
            return None

        return to_domain(model)

    def list(self) -> list[ApiKey]:
        models = self._session.scalars(select(ApiKeyModel)).all()

        return [to_domain(model) for model in models]

    def delete(
        self,
        api_key_id: UUID,
    ) -> bool:
        model = self._session.get(
            ApiKeyModel,
            api_key_id,
        )

        if model is None:
            return False

        self._session.delete(model)

        self._session.commit()

        return True

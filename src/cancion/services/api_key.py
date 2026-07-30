from uuid import UUID

from cancion.domain.api_key import ApiKey
from cancion.repositories.api_key import ApiKeyRepository


class ApiKeyService:
    """Application service for API keys."""

    def __init__(
        self,
        repository: ApiKeyRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        api_key: ApiKey,
    ) -> ApiKey:
        return self._repository.save(api_key)

    def get(
        self,
        api_key_id: UUID,
    ) -> ApiKey | None:
        return self._repository.get(api_key_id)

    def list(self) -> list[ApiKey]:
        return self._repository.list()

    def update(
        self,
        api_key: ApiKey,
    ) -> ApiKey:
        return self._repository.save(api_key)

    def delete(
        self,
        api_key_id: UUID,
    ) -> bool:
        return self._repository.delete(api_key_id)

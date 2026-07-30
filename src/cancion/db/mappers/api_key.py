from datetime import UTC, datetime

from cancion.api.schemas.api_key import ApiKeyResponse
from cancion.db.models.api_key import ApiKeyModel
from cancion.domain.api_key import ApiKey


def to_model(api_key: ApiKey) -> ApiKeyModel:
    return ApiKeyModel(
        id=api_key.id,
        agent_id=api_key.agent_id,
        name=api_key.name,
        key_hash=api_key.key_hash,
        status=api_key.status,
        created_at=api_key.created_at,
        updated_at=api_key.updated_at,
    )


def to_domain(model: ApiKeyModel) -> ApiKey:
    return ApiKey(
        id=model.id,
        agent_id=model.agent_id,
        name=model.name,
        key_hash=model.key_hash,
        status=model.status,
        created_at=_normalize_datetime(model.created_at),
        updated_at=_normalize_datetime(model.updated_at),
    )


def _normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)

    return value.astimezone(UTC)


def to_api_key_response(
    api_key: ApiKey,
) -> ApiKeyResponse:
    return ApiKeyResponse(
        id=api_key.id,
        agent_id=api_key.agent_id,
        name=api_key.name,
        key_hash=api_key.key_hash,
        status=api_key.status,
    )

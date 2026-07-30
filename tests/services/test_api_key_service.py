from uuid import uuid4

from cancion.domain.api_key import (
    ApiKey,
    ApiKeyStatus,
)
from cancion.repositories.api_key import ApiKeyRepository
from cancion.services.api_key import ApiKeyService


def make_api_key(
    agent_id=None,
    name: str = "Production",
    key_hash: str = "hashed-secret",
) -> ApiKey:
    return ApiKey(
        agent_id=agent_id or uuid4(),
        name=name,
        key_hash=key_hash,
        status=ApiKeyStatus.ACTIVE,
    )


def make_service(session):
    repository = ApiKeyRepository(session)
    return ApiKeyService(repository)


def test_create_api_key(session):
    service = make_service(session)

    api_key = make_api_key()

    created = service.create(api_key)

    assert created == api_key
    assert service.get(created.id) == api_key


def test_get_api_key(session):
    service = make_service(session)

    api_key = make_api_key()

    service.create(api_key)

    loaded = service.get(api_key.id)

    assert loaded == api_key


def test_list_api_keys(session):
    service = make_service(session)

    service.create(make_api_key(name="Production"))
    service.create(make_api_key(name="Development"))

    api_keys = service.list()

    assert len(api_keys) == 2


def test_update_api_key(session):
    service = make_service(session)

    api_key = make_api_key()

    service.create(api_key)

    updated = ApiKey(
        id=api_key.id,
        agent_id=api_key.agent_id,
        name="Production v2",
        key_hash=api_key.key_hash,
        status=api_key.status,
        created_at=api_key.created_at,
        updated_at=api_key.updated_at,
    )

    service.update(updated)

    loaded = service.get(api_key.id)

    assert loaded == updated


def test_delete_api_key(session):
    service = make_service(session)

    api_key = make_api_key()

    service.create(api_key)

    assert service.delete(api_key.id)
    assert service.get(api_key.id) is None

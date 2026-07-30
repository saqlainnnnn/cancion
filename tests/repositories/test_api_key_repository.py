from uuid import uuid4

from cancion.domain.api_key import (
    ApiKey,
    ApiKeyStatus,
)
from cancion.repositories.api_key import ApiKeyRepository


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


def test_save_api_key(session):
    repository = ApiKeyRepository(session)

    api_key = make_api_key()

    saved = repository.save(api_key)

    assert saved == api_key


def test_get_api_key(session):
    repository = ApiKeyRepository(session)

    api_key = make_api_key()

    repository.save(api_key)

    loaded = repository.get(api_key.id)

    assert loaded == api_key


def test_list_api_keys(session):
    repository = ApiKeyRepository(session)

    repository.save(make_api_key(name="Production"))
    repository.save(make_api_key(name="Development"))

    api_keys = repository.list()

    assert len(api_keys) == 2


def test_delete_api_key(session):
    repository = ApiKeyRepository(session)

    api_key = make_api_key()

    repository.save(api_key)

    assert repository.delete(api_key.id)
    assert repository.get(api_key.id) is None

from uuid import uuid4

from cancion.domain.api_key import (
    ApiKey,
    ApiKeyStatus,
)


def test_create_api_key():
    agent_id = uuid4()

    api_key = ApiKey(
        agent_id=agent_id,
        name="Production",
        key_hash="hashed-secret",
    )

    assert api_key.agent_id == agent_id
    assert api_key.name == "Production"
    assert api_key.key_hash == "hashed-secret"
    assert api_key.status == ApiKeyStatus.ACTIVE


def test_api_key_generates_id():
    api_key = ApiKey(
        agent_id=uuid4(),
        name="Production",
        key_hash="hashed-secret",
    )

    assert api_key.id is not None


def test_api_key_generates_timestamps():
    api_key = ApiKey(
        agent_id=uuid4(),
        name="Production",
        key_hash="hashed-secret",
    )

    assert api_key.created_at is not None
    assert api_key.updated_at is not None

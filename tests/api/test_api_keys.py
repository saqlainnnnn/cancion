from uuid import uuid4


def test_list_api_keys(client):
    response = client.get("/api-keys/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_api_key(client):
    response = client.post(
        "/api-keys/",
        json={
            "agent_id": str(uuid4()),
            "name": "Production",
            "key_hash": "hashed-secret",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Production"
    assert body["key_hash"] == "hashed-secret"


def test_get_api_key(client):
    created = client.post(
        "/api-keys/",
        json={
            "agent_id": str(uuid4()),
            "name": "Production",
            "key_hash": "hashed-secret",
        },
    ).json()

    response = client.get(f"/api-keys/{created['id']}")

    assert response.status_code == 200


def test_delete_api_key(client):
    created = client.post(
        "/api-keys/",
        json={
            "agent_id": str(uuid4()),
            "name": "Production",
            "key_hash": "hashed-secret",
        },
    ).json()

    response = client.delete(f"/api-keys/{created['id']}")

    assert response.status_code == 204

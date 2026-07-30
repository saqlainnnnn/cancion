from uuid import uuid4


def test_list_agents(client):
    response = client.get("/agents/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_agent(client):
    response = client.post(
        "/agents/",
        json={
            "organization_id": str(uuid4()),
            "name": "Finance Agent",
            "description": "Handles invoices",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Finance Agent"
    assert body["description"] == "Handles invoices"


def test_get_agent(client):
    created = client.post(
        "/agents/",
        json={
            "organization_id": str(uuid4()),
            "name": "Finance Agent",
            "description": "Handles invoices",
        },
    ).json()

    response = client.get(f"/agents/{created['id']}")

    assert response.status_code == 200


def test_delete_agent(client):
    created = client.post(
        "/agents/",
        json={
            "organization_id": str(uuid4()),
            "name": "Finance Agent",
            "description": "Handles invoices",
        },
    ).json()

    response = client.delete(f"/agents/{created['id']}")

    assert response.status_code == 204

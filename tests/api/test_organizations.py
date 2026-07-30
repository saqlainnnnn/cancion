from fastapi.testclient import TestClient


def test_list_organizations(client: TestClient):
    response = client.get("/organizations/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_organization(client: TestClient):
    response = client.post(
        "/organizations/",
        json={
            "name": "Acme",
            "slug": "acme",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Acme"
    assert body["slug"] == "acme"


def test_get_organization(client: TestClient):
    created = client.post(
        "/organizations/",
        json={
            "name": "Acme",
            "slug": "acme",
        },
    ).json()

    response = client.get(f"/organizations/{created['id']}")

    assert response.status_code == 200


def test_delete_organization(client: TestClient):
    created = client.post(
        "/organizations/",
        json={
            "name": "Acme",
            "slug": "acme",
        },
    ).json()

    response = client.delete(f"/organizations/{created['id']}")

    assert response.status_code == 204

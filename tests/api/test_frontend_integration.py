from fastapi.testclient import TestClient

from cancion.api.app import app


def test_app_allows_frontend_dev_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"

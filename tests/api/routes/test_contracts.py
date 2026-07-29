from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from cancion.api.app import app
from cancion.api.dependencies import (
    get_contract_service,
    get_intent_parser,
)
from cancion.common import Action, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.domain.intent import Intent
from cancion.intent.exceptions import IntentParseError


class FailingParser:
    def parse(self, message: str):
        raise IntentParseError("Unable to parse request")


class FakeParser:
    def parse(self, message: str) -> Intent:
        return Intent(
            vendor="Amazon",
            action=Action.PAY,
            max_amount=Money(Decimal("100.00")),
            frequency=Frequency.MONTHLY,
        )


class FakeContractService:
    def create(self, intent: Intent) -> Contract:
        return Contract(
            vendor=intent.vendor,
            action=intent.action,
            max_amount=intent.max_amount,
            frequency=intent.frequency,
            approval_mode=intent.approval_mode,
        )


def test_create_contract():
    app.dependency_overrides[get_intent_parser] = lambda: FakeParser()
    app.dependency_overrides[get_contract_service] = lambda: FakeContractService()

    client = TestClient(app)

    response = client.post(
        "/contracts/",
        json={"text": "Pay Amazon $100 monthly"},
    )

    assert response.status_code == 201

    body = response.json()

    assert body["vendor"] == "Amazon"
    assert body["action"] == "pay"
    assert body["max_amount"]["amount"] == "100.00"

    app.dependency_overrides.clear()


def test_create_contract_returns_400_when_parse_fails():
    app.dependency_overrides[get_intent_parser] = lambda: FailingParser()
    app.dependency_overrides[get_contract_service] = lambda: FakeContractService()

    client = TestClient(app)

    response = client.post(
        "/contracts/",
        json={"text": "asdfghjkl"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Unable to parse request"}

    app.dependency_overrides.clear()


def test_list_contracts():
    contract = Contract(
        vendor="Amazon",
        action=Action.PAY,
        max_amount=Money(Decimal("100.00")),
        frequency=Frequency.MONTHLY,
    )

    class FakeService:
        def list(self):
            return [contract]

    app.dependency_overrides[get_contract_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.get("/contracts/")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1

    assert body[0]["vendor"] == "Amazon"
    assert body[0]["action"] == "pay"
    assert body[0]["max_amount"]["amount"] == "100.00"


def test_get_contract():
    contract = Contract(
        vendor="Amazon",
        action=Action.PAY,
        max_amount=Money(Decimal("100.00")),
        frequency=Frequency.MONTHLY,
    )

    class FakeService:
        def get(self, contract_id):
            return contract

    app.dependency_overrides[get_contract_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.get(f"/contracts/{contract.id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == str(contract.id)
    assert body["vendor"] == "Amazon"


def test_get_contract_returns_404():
    class FakeService:
        def get(self, contract_id):
            return None

    app.dependency_overrides[get_contract_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.get(f"/contracts/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Contract not found",
    }


def test_update_contract():
    contract = Contract(
        vendor="Netflix",
        action=Action.RENEW,
        max_amount=Money(Decimal("20")),
        frequency=Frequency.MONTHLY,
    )

    updated = contract.update(
        vendor="Spotify",
        max_amount=Money(Decimal("30")),
    )

    class FakeService:
        def update(self, contract_id, update):
            return updated

    app.dependency_overrides[get_contract_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.put(
        f"/contracts/{contract.id}",
        json={
            "vendor": "Spotify",
            "max_amount": "30",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["vendor"] == "Spotify"
    assert body["version"] == 2

    app.dependency_overrides.clear()


def test_update_contract_returns_404():
    class FakeService:
        def update(self, contract_id, update):
            return None

    app.dependency_overrides[get_contract_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.put(
        f"/contracts/{uuid4()}",
        json={},
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Contract not found",
    }

    app.dependency_overrides.clear()


def test_delete_contract():
    class FakeService:
        def delete(self, contract_id):
            return True

    app.dependency_overrides[get_contract_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.delete(f"/contracts/{uuid4()}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_contract_returns_404():
    class FakeService:
        def delete(self, contract_id):
            return False

    app.dependency_overrides[get_contract_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.delete(f"/contracts/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Contract not found",
    }

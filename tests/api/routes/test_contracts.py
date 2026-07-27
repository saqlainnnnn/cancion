from decimal import Decimal

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

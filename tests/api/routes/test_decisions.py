from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from cancion.api.app import app
from cancion.api.dependencies import get_decision_service
from cancion.common import Action
from cancion.common.money import Money
from cancion.domain.decision import Decision, DecisionOutcome
from cancion.domain.decision_record import DecisionRecord


def make_record():
    return DecisionRecord(
        id=uuid4(),
        contract_id=uuid4(),
        vendor="Amazon",
        action=Action.PAY,
        amount=Money(Decimal("100")),
        decision=Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=[],
        ),
        created_at=datetime.now(UTC),
    )


def test_list_decisions():
    record = make_record()

    class FakeService:
        def list(self):
            return [record]

    app.dependency_overrides[get_decision_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.get("/decisions/")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["vendor"] == "Amazon"
    assert body[0]["outcome"] == "approve"

    app.dependency_overrides.clear()


def test_get_decision():
    record = make_record()

    class FakeService:
        def get(self, _):
            return record

    app.dependency_overrides[get_decision_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.get(f"/decisions/{record.id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == str(record.id)
    assert body["vendor"] == "Amazon"

    app.dependency_overrides.clear()


def test_get_decision_returns_404():
    class FakeService:
        def get(self, _):
            return None

    app.dependency_overrides[get_decision_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.get(f"/decisions/{uuid4()}")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Decision not found",
    }

    app.dependency_overrides.clear()


def test_list_contract_decisions():
    record = make_record()

    class FakeService:
        def list_by_contract(self, _):
            return [record]

    app.dependency_overrides[get_decision_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.get(f"/decisions/contracts/{record.contract_id}")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["contract_id"] == str(record.contract_id)

    app.dependency_overrides.clear()


def test_delete_decision():
    class FakeService:
        def delete(self, _):
            return True

    app.dependency_overrides[get_decision_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.delete(f"/decisions/{uuid4()}")

    assert response.status_code == 204

    app.dependency_overrides.clear()


def test_delete_decision_returns_404():
    class FakeService:
        def delete(self, _):
            return False

    app.dependency_overrides[get_decision_service] = lambda: FakeService()

    client = TestClient(app)

    response = client.delete(f"/decisions/{uuid4()}")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Decision not found",
    }

    app.dependency_overrides.clear()

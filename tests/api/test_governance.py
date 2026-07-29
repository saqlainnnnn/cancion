from decimal import Decimal
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from cancion.api.app import app
from cancion.api.dependencies import (
    get_contract_service,
    get_governance_service,
)
from cancion.common import (
    Action,
    ApprovalMode,
    Frequency,
)
from cancion.common.money import Money
from cancion.domain.contract import Contract, ContractStatus
from cancion.domain.decision import (
    Decision,
    DecisionOutcome,
)


class FakeContractService:
    def get(self, contract_id):
        return Contract(
            id=contract_id,
            vendor="Netflix",
            action=Action.PAY,
            max_amount=Money(
                amount=Decimal("25.00"),
                currency="USD",
            ),
            frequency=Frequency.MONTHLY,
            approval_mode=ApprovalMode.AUTO,
            status=ContractStatus.ACTIVE,
            version=1,
            agent_id="agent-1",
        )


class FakeGovernanceService:
    def evaluate(self, contract, request):
        return Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=["Approved"],
        )


@pytest.fixture
def client():
    app.dependency_overrides[get_contract_service] = lambda: FakeContractService()
    app.dependency_overrides[get_governance_service] = lambda: FakeGovernanceService()

    with TestClient(app) as client:
        yield client


def test_evaluate(client: TestClient):
    contract_id = str(uuid4())

    response = client.post(
        "/governance/evaluate",
        json={
            "contract_id": contract_id,
            "vendor": "Netflix",
            "action": "pay",
            "amount": {
                "amount": "20.00",
                "currency": "USD",
            },
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "outcome": "approve",
        "reasons": [
            "Approved",
        ],
    }

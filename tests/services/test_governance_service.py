from decimal import Decimal
from unittest.mock import Mock

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.domain.decision import DecisionOutcome
from cancion.governance.context import SpendRequest
from cancion.governance.engine import GovernanceEngine
from cancion.governance.policies.action import ActionRule
from cancion.governance.policies.amount import AmountRule
from cancion.governance.policies.approval import ApprovalRule
from cancion.governance.policies.status import StatusRule
from cancion.governance.policies.vendor import VendorRule
from cancion.repositories.decision import DecisionRepository
from cancion.services.governance import GovernanceService


def make_service() -> GovernanceService:
    engine = GovernanceEngine(
        [
            VendorRule(),
            ActionRule(),
            AmountRule(),
            StatusRule(),
            ApprovalRule(),
        ]
    )

    repository = Mock(spec=DecisionRepository)

    return GovernanceService(
        engine=engine,
        repository=repository,
    )


def make_contract(
    *,
    vendor: str = "Netflix",
    approval_mode: ApprovalMode = ApprovalMode.AUTO,
) -> Contract:
    return Contract(
        vendor=vendor,
        action=Action.RENEW,
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=approval_mode,
    )


def make_request(
    *,
    vendor: str = "Netflix",
    amount: str = "15",
) -> SpendRequest:
    return SpendRequest(
        vendor=vendor,
        action=Action.RENEW,
        amount=Money(Decimal(amount)),
    )


def test_service_approves_valid_request() -> None:
    service = make_service()

    decision = service.evaluate(
        make_contract(),
        make_request(),
    )

    assert decision.outcome is DecisionOutcome.APPROVE
    assert decision.reasons == []


def test_service_denies_vendor_mismatch() -> None:
    service = make_service()

    decision = service.evaluate(
        make_contract(),
        make_request(vendor="Spotify"),
    )

    assert decision.outcome is DecisionOutcome.DENY
    assert decision.reasons == ["Vendor mismatch: expected Netflix, got Spotify."]


def test_service_denies_amount_exceeded() -> None:
    service = make_service()

    decision = service.evaluate(
        make_contract(),
        make_request(amount="25"),
    )

    assert decision.outcome is DecisionOutcome.DENY
    assert decision.reasons == ["Amount exceeds policy: USD 25 > USD 18."]


def test_service_escalates_manual_approval() -> None:
    service = make_service()

    decision = service.evaluate(
        make_contract(
            approval_mode=ApprovalMode.MANUAL,
        ),
        make_request(),
    )

    assert decision.outcome is DecisionOutcome.ESCALATE
    assert decision.reasons == ["Manual approval required."]

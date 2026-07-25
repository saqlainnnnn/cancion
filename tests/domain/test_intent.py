from decimal import Decimal

import pytest

from cancion.common.money import Money
from cancion.domain.intent import ApprovalMode, Frequency, Intent


def test_create_intent():
    intent = Intent(
        vendor="Netflix",
        action="renew",
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
    )

    assert intent.vendor == "Netflix"
    assert intent.action == "renew"
    assert intent.max_amount == Money(Decimal("18"))
    assert intent.frequency == Frequency.MONTHLY
    assert intent.approval_mode == ApprovalMode.AUTO


def test_intent_is_immutable():
    intent = Intent(
        vendor="Netflix",
        action="renew",
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
    )

    with pytest.raises(AttributeError):
        intent.vendor = "Spotify"  # type: ignore[misc]

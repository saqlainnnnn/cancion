from decimal import Decimal

import pytest

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.intent.builder import IntentBuilder
from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent


def test_build_success() -> None:
    parsed = ParsedIntent(
        vendor="Netflix",
        action=Action.RENEW,
        amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
    )

    intent = IntentBuilder.build(parsed)

    assert intent.vendor == "Netflix"
    assert intent.action is Action.RENEW
    assert intent.max_amount == Money(Decimal("18"))
    assert intent.frequency == Frequency.MONTHLY


@pytest.mark.parametrize(
    "field",
    [
        "vendor",
        "action",
        "amount",
        "frequency",
    ],
)
def test_missing_required_fields(field: str) -> None:
    parsed = ParsedIntent(
        vendor="Netflix",
        action=Action.RENEW,
        amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
    )

    setattr(parsed, field, None)

    with pytest.raises(IntentParseError):
        IntentBuilder.build(parsed)

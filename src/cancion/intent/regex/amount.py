import re
from decimal import Decimal

from cancion.common.money import Money
from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent

_AMOUNT_PATTERN = re.compile(r"\$(\d+(?:\.\d+)?)")


def extract_amount(message: str, parsed: ParsedIntent) -> None:
    """Populate the amount field."""

    match = _AMOUNT_PATTERN.search(message)

    if match is None:
        raise IntentParseError("Unable to determine amount.")

    parsed.amount = Money(
        amount=Decimal(match.group(1)),
        currency="USD",
    )

import re
from decimal import Decimal

from cancion.common import Action
from cancion.intent.exceptions import IntentParseError
from cancion.intent.regex.patterns import ACTION_PATTERNS

_AMOUNT_PATTERN = re.compile(r"\$(\d+(?:\.\d+)?)")


def extract_action(message: str) -> Action:
    message = message.lower()

    for action, keywords in ACTION_PATTERNS.items():
        if any(keyword in message for keyword in keywords):
            return action

    raise IntentParseError("Unable to determine action.")


def extract_amount(message: str) -> Decimal:
    match = _AMOUNT_PATTERN.search(message)

    if match is None:
        raise IntentParseError("Unable to determine amount.")

    return Decimal(match.group(1))

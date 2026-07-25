from cancion.common import Frequency
from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent

FREQUENCY_PATTERNS: dict[Frequency, tuple[str, ...]] = {
    Frequency.DAILY: (
        "daily",
        "every day",
        "each day",
    ),
    Frequency.WEEKLY: (
        "weekly",
        "every week",
        "each week",
    ),
    Frequency.MONTHLY: (
        "monthly",
        "every month",
        "each month",
    ),
    Frequency.YEARLY: (
        "yearly",
        "annually",
        "every year",
        "each year",
    ),
}


def extract_frequency(message: str, parsed: ParsedIntent) -> None:
    """Populate the frequency field."""

    message = message.lower()

    for frequency, keywords in FREQUENCY_PATTERNS.items():
        if any(keyword in message for keyword in keywords):
            parsed.frequency = frequency
            return

    raise IntentParseError("Unable to determine frequency.")

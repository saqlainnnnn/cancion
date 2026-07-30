from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent
from cancion.intent.regex.vendors import KNOWN_VENDORS


def extract_vendor(message: str, parsed: ParsedIntent) -> None:
    """Populate the vendor field."""

    words = [
        word.strip(".,!?()[]{}\"'")
        for word in message.lower().split()
        if word.strip(".,!?()[]{}\"'")
    ]

    if not words:
        raise IntentParseError("Unable to determine vendor.")

    known_matches = sorted(KNOWN_VENDORS & set(words))
    if known_matches:
        parsed.vendor = known_matches[0].title()
        return

    ignored = {"renew", "cancel", "buy", "pay", "subscribe", "for", "the", "a", "an"}
    candidate = next((word for word in words[1:] if word not in ignored), None)

    if candidate is None:
        candidate = words[0]

    parsed.vendor = candidate.title()

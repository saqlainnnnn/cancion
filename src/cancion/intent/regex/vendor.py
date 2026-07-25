from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent
from cancion.intent.regex.vendors import KNOWN_VENDORS


def extract_vendor(message: str, parsed: ParsedIntent) -> None:
    """Populate the vendor field."""

    words = {word.strip(".,!?()[]{}\"'") for word in message.lower().split()}

    matches = KNOWN_VENDORS & words

    if not matches:
        raise IntentParseError("Unable to determine vendor.")

    parsed.vendor = sorted(matches)[0].title()

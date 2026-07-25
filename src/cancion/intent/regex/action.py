from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent
from cancion.intent.regex.patterns import ACTION_PATTERNS


def extract_action(message: str, parsed: ParsedIntent) -> None:
    """Populate the action field."""

    message = message.lower()

    for action, keywords in ACTION_PATTERNS.items():
        if any(keyword in message for keyword in keywords):
            parsed.action = action
            return

    raise IntentParseError("Unable to determine action.")

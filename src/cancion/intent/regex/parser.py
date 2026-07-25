from cancion.domain.intent import Intent
from cancion.intent.builder import IntentBuilder
from cancion.intent.parsed_intent import ParsedIntent
from cancion.intent.protocol import IntentParser
from cancion.intent.regex.action import extract_action
from cancion.intent.regex.amount import extract_amount
from cancion.intent.regex.frequency import extract_frequency
from cancion.intent.regex.vendor import extract_vendor


class RegexIntentParser(IntentParser):
    """Deterministic regex parser."""

    def parse(self, message: str) -> Intent:
        parsed = ParsedIntent()

        extract_action(message, parsed)
        extract_amount(message, parsed)
        extract_frequency(message, parsed)
        extract_vendor(message, parsed)

        return IntentBuilder.build(parsed)

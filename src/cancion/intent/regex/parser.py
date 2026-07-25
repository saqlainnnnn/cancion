from cancion.domain.intent import Intent
from cancion.intent.parsed_intent import ParsedIntent
from cancion.intent.protocol import IntentParser
from cancion.intent.regex.action import extract_action
from cancion.intent.regex.amount import extract_amount
from cancion.intent.regex.frequency import extract_frequency


class RegexIntentParser(IntentParser):
    """Deterministic regex parser."""

    def parse(self, message: str) -> Intent:
        parsed = ParsedIntent()

        extract_action(message, parsed)
        extract_amount(message, parsed)
        extract_frequency(message, parsed)

        if (
            parsed.action is None
            or parsed.amount is None
            or parsed.frequency is None
            or parsed.vendor is None
        ):
            raise ValueError("Parser produced an incomplete intent.")

        return Intent(
            vendor=parsed.vendor,
            action=parsed.action.value,
            max_amount=parsed.amount,
            frequency=parsed.frequency,
            approval_mode=parsed.approval_mode,
        )

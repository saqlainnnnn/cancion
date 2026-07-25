from cancion.domain.intent import Intent
from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent


class IntentBuilder:
    """Builds a validated Intent from a ParsedIntent."""

    @staticmethod
    def build(parsed: ParsedIntent) -> Intent:
        if parsed.vendor is None:
            raise IntentParseError("Vendor is required.")

        if parsed.action is None:
            raise IntentParseError("Action is required.")

        if parsed.amount is None:
            raise IntentParseError("Amount is required.")

        if parsed.frequency is None:
            raise IntentParseError("Frequency is required.")

        return Intent(
            vendor=parsed.vendor,
            action=parsed.action.value,
            max_amount=parsed.amount,
            frequency=parsed.frequency,
            approval_mode=parsed.approval_mode,
        )

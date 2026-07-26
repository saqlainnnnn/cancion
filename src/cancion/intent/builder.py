from typing import TypeVar

from cancion.domain.intent import Intent
from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent

T = TypeVar("T")


class IntentBuilder:
    """Builds a validated Intent from a ParsedIntent."""

    @staticmethod
    def _require(value: T | None, message: str) -> T:
        """Return a required value or raise an IntentParseError."""
        if value is None:
            raise IntentParseError(message)
        return value

    @classmethod
    def build(cls, parsed: ParsedIntent) -> Intent:
        return Intent(
            vendor=cls._require(parsed.vendor, "Vendor is required."),
            action=cls._require(parsed.action, "Action is required."),
            max_amount=cls._require(parsed.amount, "Amount is required."),
            frequency=cls._require(parsed.frequency, "Frequency is required."),
            approval_mode=parsed.approval_mode,
        )

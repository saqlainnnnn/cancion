import pytest

from cancion.common import Frequency
from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent
from cancion.intent.regex.frequency import extract_frequency


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("renew every day", Frequency.DAILY),
        ("renew weekly", Frequency.WEEKLY),
        ("renew every month", Frequency.MONTHLY),
        ("renew annually", Frequency.YEARLY),
    ],
)
def test_extract_frequency(message: str, expected: Frequency) -> None:
    parsed = ParsedIntent()

    extract_frequency(message, parsed)

    assert parsed.frequency == expected


def test_unknown_frequency() -> None:
    parsed = ParsedIntent()

    with pytest.raises(IntentParseError):
        extract_frequency("renew netflix", parsed)

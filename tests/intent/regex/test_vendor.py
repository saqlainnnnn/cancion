import pytest

from cancion.intent.exceptions import IntentParseError
from cancion.intent.parsed_intent import ParsedIntent
from cancion.intent.regex.vendor import extract_vendor


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Renew Netflix", "Netflix"),
        ("Cancel Spotify", "Spotify"),
        ("Buy from Amazon", "Amazon"),
        ("Pay OpenAI", "Openai"),
    ],
)
def test_extract_vendor(message: str, expected: str) -> None:
    parsed = ParsedIntent()

    extract_vendor(message, parsed)

    assert parsed.vendor == expected


def test_unknown_vendor() -> None:
    parsed = ParsedIntent()

    with pytest.raises(IntentParseError):
        extract_vendor("Renew unknown service", parsed)

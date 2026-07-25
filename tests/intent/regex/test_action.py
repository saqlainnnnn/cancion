import pytest

from cancion.common import Action
from cancion.intent.exceptions import IntentParseError
from cancion.intent.regex.extractors import extract_action


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Renew my Netflix subscription", Action.RENEW),
        ("Buy groceries", Action.BUY),
        ("Pay my electricity bill", Action.PAY),
        ("Cancel Spotify", Action.CANCEL),
    ],
)
def test_extract_action(message: str, expected: Action) -> None:
    assert extract_action(message) == expected


def test_unknown_action() -> None:
    with pytest.raises(IntentParseError):
        extract_action("The weather is nice today")

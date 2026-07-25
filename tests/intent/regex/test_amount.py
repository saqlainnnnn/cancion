from decimal import Decimal

import pytest

from cancion.intent.exceptions import IntentParseError
from cancion.intent.regex.extractors import extract_amount


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("under $18", Decimal("18")),
        ("below $25.99", Decimal("25.99")),
        ("for $100", Decimal("100")),
        ("maximum $9.50", Decimal("9.50")),
    ],
)
def test_extract_amount(message: str, expected: Decimal) -> None:
    assert extract_amount(message) == expected


def test_missing_amount() -> None:
    with pytest.raises(IntentParseError):
        extract_amount("Renew Netflix")

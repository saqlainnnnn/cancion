from datetime import UTC, datetime

import pytest

from cancion.domain.period import Period


def test_contains():
    period = Period(
        start=datetime(2026, 7, 1, tzinfo=UTC),
        end=datetime(2026, 8, 1, tzinfo=UTC),
    )

    assert period.contains(
        datetime(2026, 7, 15, tzinfo=UTC),
    )


def test_does_not_contain():
    period = Period(
        start=datetime(2026, 7, 1, tzinfo=UTC),
        end=datetime(2026, 8, 1, tzinfo=UTC),
    )

    assert not period.contains(
        datetime(2026, 8, 5, tzinfo=UTC),
    )


def test_invalid_period():
    with pytest.raises(ValueError):
        Period(
            start=datetime(2026, 8, 1, tzinfo=UTC),
            end=datetime(2026, 7, 1, tzinfo=UTC),
        )

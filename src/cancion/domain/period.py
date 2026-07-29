from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class Period:
    """Represents a bounded billing period."""

    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "start", self._normalize(self.start))
        object.__setattr__(self, "end", self._normalize(self.end))

        if self.start >= self.end:
            raise ValueError("Period start must be before period end.")

    def contains(self, instant: datetime) -> bool:
        instant = self._normalize(instant)
        return self.start <= instant < self.end

    @staticmethod
    def _normalize(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)

        return dt.astimezone(UTC)

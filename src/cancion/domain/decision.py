from dataclasses import dataclass
from enum import StrEnum


class DecisionOutcome(StrEnum):
    APPROVE = "approve"
    DENY = "deny"
    ESCALATE = "escalate"


@dataclass(frozen=True, slots=True)
class Decision:
    """Result of evaluating a spend request."""

    outcome: DecisionOutcome
    reasons: list[str]

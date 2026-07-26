from dataclasses import dataclass
from enum import StrEnum


class RuleOutcome(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    ESCALATE = "escalate"


@dataclass(frozen=True, slots=True)
class RuleResult:
    outcome: RuleOutcome
    reason: str | None = None

    @classmethod
    def passed(cls) -> "RuleResult":
        return cls(RuleOutcome.PASS)

    @classmethod
    def failed(cls, reason: str) -> "RuleResult":
        return cls(RuleOutcome.FAIL, reason)

    @classmethod
    def escalated(cls, reason: str) -> "RuleResult":
        return cls(RuleOutcome.ESCALATE, reason)

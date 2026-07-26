from dataclasses import dataclass

from cancion.common import Action
from cancion.common.money import Money
from cancion.domain.contract import Contract


@dataclass(frozen=True, slots=True)
class SpendRequest:
    """Represents an incoming spend request from an AI agent."""

    vendor: str
    action: Action
    amount: Money


@dataclass(frozen=True, slots=True)
class EvaluationContext:
    """Input for governance evaluation."""

    contract: Contract
    request: SpendRequest

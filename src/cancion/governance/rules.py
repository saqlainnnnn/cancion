from abc import ABC, abstractmethod

from cancion.governance.context import EvaluationContext


class Rule(ABC):
    """Base class for governance rules."""

    @abstractmethod
    def evaluate(self, context: EvaluationContext) -> str | None:
        """
        Return a failure reason if the rule fails.
        Return None if the rule passes.
        """

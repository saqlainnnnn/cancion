from abc import ABC, abstractmethod

from cancion.governance.context import EvaluationContext
from cancion.governance.rule_result import RuleResult


class Rule(ABC):
    @abstractmethod
    def evaluate(self, context: EvaluationContext) -> RuleResult: ...

from cancion.common import ApprovalMode
from cancion.governance.context import EvaluationContext
from cancion.governance.rule_result import RuleResult
from cancion.governance.rules import Rule


class ApprovalRule(Rule):
    """Determines whether a spend request requires manual approval."""

    def evaluate(self, context: EvaluationContext) -> RuleResult:
        if context.contract.approval_mode is ApprovalMode.MANUAL:
            return RuleResult.escalated("Manual approval required.")

        return RuleResult.passed()

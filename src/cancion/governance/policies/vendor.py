from cancion.governance.context import EvaluationContext
from cancion.governance.rule_result import RuleResult
from cancion.governance.rules import Rule


class VendorRule(Rule):
    """Ensures the spend request targets the expected vendor."""

    def evaluate(self, context: EvaluationContext) -> RuleResult:
        if context.contract.vendor.lower() != context.request.vendor.lower():
            return RuleResult.failed(
                f"Vendor mismatch: expected "
                f"{context.contract.vendor}, "
                f"got {context.request.vendor}."
            )

        return RuleResult.passed()

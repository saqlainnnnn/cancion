from cancion.governance.context import EvaluationContext
from cancion.governance.rules import Rule


class VendorRule(Rule):
    """Ensures the spend request targets the expected vendor."""

    def evaluate(self, context: EvaluationContext) -> str | None:
        if context.contract.vendor.lower() != context.request.vendor.lower():
            return (
                f"Vendor mismatch: expected "
                f"{context.contract.vendor}, "
                f"got {context.request.vendor}."
            )

        return None

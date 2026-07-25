from cancion.domain.contract import Contract
from cancion.domain.intent import Intent


class ContractFactory:
    """Creates Contracts from validated Intents."""

    @staticmethod
    def create(intent: Intent) -> Contract:
        return Contract(
            agent_id=None,  # Placeholder until agents exist
            vendor=intent.vendor,
            action=intent.action,
            max_amount=intent.max_amount,
            frequency=intent.frequency,
            approval_mode=intent.approval_mode,
        )

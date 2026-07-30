from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from cancion.db.session import SessionLocal
from cancion.domain.factory import ContractFactory
from cancion.governance.engine import GovernanceEngine
from cancion.governance.policies.action import ActionRule
from cancion.governance.policies.amount import AmountRule
from cancion.governance.policies.approval import ApprovalRule
from cancion.governance.policies.frequency import FrequencyRule
from cancion.governance.policies.status import StatusRule
from cancion.governance.policies.vendor import VendorRule
from cancion.intent.protocol import IntentParser
from cancion.intent.regex.parser import RegexIntentParser
from cancion.repositories.contract import ContractRepository
from cancion.repositories.decision import DecisionRepository
from cancion.repositories.organization import OrganizationRepository
from cancion.repositories.spend_ledger import SpendLedgerRepository
from cancion.services.contract import ContractService
from cancion.services.decision import DecisionService
from cancion.services.governance import GovernanceService
from cancion.services.organization import OrganizationService
from cancion.services.spend_ledger import SpendLedgerService


def get_intent_parser() -> IntentParser:
    """Create the application's intent parser."""
    return RegexIntentParser()


def get_db() -> Generator[Session]:
    """Provide a database session for a request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_contract_repository(
    db: Session = Depends(get_db),
) -> ContractRepository:
    """Create a contract repository."""
    return ContractRepository(db)


def get_decision_repository(
    db: Session = Depends(get_db),
) -> DecisionRepository:
    """Create a decision repository."""
    return DecisionRepository(db)


def get_spend_ledger_repository(
    db: Session = Depends(get_db),
) -> SpendLedgerRepository:
    """Create a spend ledger repository."""
    return SpendLedgerRepository(db)


def get_contract_service(
    repository: ContractRepository = Depends(get_contract_repository),
) -> ContractService:
    """Create the contract application service."""
    return ContractService(
        repository=repository,
        factory=ContractFactory(),
    )


def get_decision_service(
    repository: DecisionRepository = Depends(get_decision_repository),
) -> DecisionService:
    """Create the decision application service."""
    return DecisionService(
        repository=repository,
    )


def get_spend_ledger_service(
    repository: SpendLedgerRepository = Depends(
        get_spend_ledger_repository,
    ),
) -> SpendLedgerService:
    """Create the spend ledger application service."""
    return SpendLedgerService(
        repository=repository,
    )


def get_governance_engine(
    ledger_service: SpendLedgerService = Depends(
        get_spend_ledger_service,
    ),
) -> GovernanceEngine:
    """Create the governance engine."""
    return GovernanceEngine(
        [
            VendorRule(),
            ActionRule(),
            AmountRule(),
            StatusRule(),
            ApprovalRule(),
            FrequencyRule(ledger_service),
        ]
    )


def get_governance_service(
    engine: GovernanceEngine = Depends(
        get_governance_engine,
    ),
    repository: DecisionRepository = Depends(
        get_decision_repository,
    ),
    ledger_service: SpendLedgerService = Depends(
        get_spend_ledger_service,
    ),
) -> GovernanceService:
    """Create the governance application service."""
    return GovernanceService(
        engine=engine,
        repository=repository,
        ledger_service=ledger_service,
    )


def get_organization_repository(
    db: Session = Depends(get_db),
) -> OrganizationRepository:
    return OrganizationRepository(db)


def get_organization_service(
    repository: OrganizationRepository = Depends(
        get_organization_repository,
    ),
) -> OrganizationService:
    return OrganizationService(repository)

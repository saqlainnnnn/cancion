from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from cancion.db.session import SessionLocal
from cancion.domain.factory import ContractFactory
from cancion.intent.protocol import IntentParser
from cancion.intent.regex.parser import RegexIntentParser
from cancion.repositories.contract import ContractRepository
from cancion.services.contract import ContractService
from cancion.services.governance import GovernanceService


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


def get_contract_service(
    repository: ContractRepository = Depends(get_contract_repository),
) -> ContractService:
    """Create the contract application service."""
    return ContractService(
        repository=repository,
        factory=ContractFactory(),
    )


def get_governance_service() -> GovernanceService:
    """Create the governance application service."""
    return GovernanceService()

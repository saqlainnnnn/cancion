from collections.abc import Generator

from sqlalchemy.orm import Session

from cancion.db.session import SessionLocal
from cancion.domain.factory import ContractFactory
from cancion.repositories.contract import ContractRepository
from cancion.services.contract import ContractService
from cancion.services.governance import GovernanceService


def get_db() -> Generator[Session]:
    """Provide a database session for a request."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_contract_repository(
    db: Session,
) -> ContractRepository:
    """Create a contract repository."""

    return ContractRepository(db)


def get_contract_service(
    repository: ContractRepository,
) -> ContractService:
    """Create the contract application service."""

    return ContractService(
        repository=repository,
        factory=ContractFactory(),
    )


def get_governance_service() -> GovernanceService:
    """Create the governance application service."""

    return GovernanceService()

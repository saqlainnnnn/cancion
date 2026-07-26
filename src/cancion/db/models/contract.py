from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from cancion.common import Action, ApprovalMode, Frequency
from cancion.db.base import Base
from cancion.domain.contract import ContractStatus


class ContractModel(Base):
    __tablename__ = "contracts"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    vendor: Mapped[str] = mapped_column(String(255))

    action: Mapped[Action] = mapped_column(Enum(Action))

    max_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    frequency: Mapped[Frequency] = mapped_column(Enum(Frequency))

    approval_mode: Mapped[ApprovalMode] = mapped_column(Enum(ApprovalMode))

    status: Mapped[ContractStatus] = mapped_column(Enum(ContractStatus))

    version: Mapped[int]

    agent_id: Mapped[UUID | None]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

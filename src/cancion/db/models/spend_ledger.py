from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from cancion.db.base import Base


class SpendLedgerModel(Base):
    __tablename__ = "spend_ledgers"

    __table_args__ = (
        UniqueConstraint(
            "contract_id",
            "period_start",
            name="uq_spend_ledger_period",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)

    contract_id: Mapped[UUID]

    period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    spent_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    currency: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

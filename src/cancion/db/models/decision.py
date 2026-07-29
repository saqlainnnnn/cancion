from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, Enum, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cancion.common import Action
from cancion.db.base import Base
from cancion.domain.decision import DecisionOutcome


class DecisionModel(Base):
    __tablename__ = "decisions"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )

    contract_id: Mapped[UUID] = mapped_column(
        Uuid,
        nullable=False,
        index=True,
    )

    vendor: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    action: Mapped[Action] = mapped_column(
        Enum(Action),
        nullable=False,
    )

    amount: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    outcome: Mapped[DecisionOutcome] = mapped_column(
        Enum(DecisionOutcome),
        nullable=False,
    )

    reasons: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

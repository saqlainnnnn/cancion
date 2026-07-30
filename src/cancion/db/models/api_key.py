from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from cancion.db.base import Base
from cancion.domain.api_key import ApiKeyStatus


class ApiKeyModel(Base):
    __tablename__ = "api_keys"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    agent_id: Mapped[UUID] = mapped_column(
        ForeignKey("agents.id"),
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )

    key_hash: Mapped[str] = mapped_column(
        String(255),
    )

    status: Mapped[ApiKeyStatus] = mapped_column(
        Enum(ApiKeyStatus),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

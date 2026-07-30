from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cancion.core.config import settings
from cancion.db.base import Base
from cancion.db.models import contract, decision, spend_ledger  # noqa: F401

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

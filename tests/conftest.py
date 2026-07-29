from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from cancion.api.app import app
from cancion.db.base import Base


@pytest.fixture(autouse=True)
def clear_dependency_overrides() -> Generator[None]:
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def session() -> Generator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)

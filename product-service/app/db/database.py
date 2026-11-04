from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings

_engine = None
_session_factory = None


def init_db(database_url: str) -> None:
    global _engine, _session_factory
    settings = get_settings()

    _engine = create_engine(
        str(database_url),
        echo=settings.db_echo,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    _session_factory = sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        autoflush=False,
    )


def close_connection() -> None:
    global _engine
    if _engine:
        _engine.dispose()


def get_db_session() -> Generator[Session, None, None]:
    if _session_factory is None:
        raise RuntimeError("DB not initialized")

    with _session_factory() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

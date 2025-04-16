from sqlalchemy import create_engine
from functools import lru_cache
from sqlalchemy.orm import sessionmaker
from loaders.config import BaseLLMSettings


@lru_cache(maxsize=None)
def session_maker(connection_string: str):
    engine = create_engine(connection_string)
    maker = sessionmaker()
    maker.configure(bind=engine)
    return maker


def create_db_session(settings: BaseLLMSettings):
    if not settings.SQLALCHEMY_CONNECTION_STRING:
        raise RuntimeError("SQLALCHEMY_CONNECTION_STRING is not set, but required for database operations")
    maker = session_maker(settings.SQLALCHEMY_CONNECTION_STRING)
    session = maker()
    return session

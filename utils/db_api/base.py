from data.config import DATABASE_URL

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager
import typing


engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)


@as_declarative(metadata=metadata)
class Base:
    pass


Session = sessionmaker()


@contextmanager
def session(**kwargs) -> typing.ContextManager[Session]:
    new_session = Session(**kwargs)

    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()

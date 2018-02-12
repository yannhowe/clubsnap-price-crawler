import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from camprice import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_threads_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Threads(DeclarativeBase):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    thread_id = Column('thread_id', Integer, nullable=True)
    title = Column('title', String, nullable=True)
    link = Column('link', String, nullable=True)
    username = Column('username', String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

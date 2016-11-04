from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
import settings


DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_ubuntu_table(engine):
    return DeclarativeBase.metadata.create_all(engine)


class ubuntuDB(DeclarativeBase):
    __tablename__ = "askUbuntu"
    id = Column('id', Integer, primary_key = True)
    tags = Column('tags', Text, nullable = True)
    questions = Column('questions', Text, nullable = False)
    votes = Column('votes', Text, nullable = True)
    no_answers = Column('no_answers', Text, nullable = True)
    links = Column('links', Text, nullable = False)

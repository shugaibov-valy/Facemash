import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import sqlalchemy as sq
from sqlalchemy.dialects.postgresql import UUID
from settings import config
from datetime import datetime


engine = create_engine(config.alchemy_url)

# Session object
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class object for model class
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__: str = 'users'

    id = sq.Column(sq.Integer(), primary_key=True)
    vk_id = sq.Column(sq.Integer())
    photo = sq.Column(sq.String(1024))
    rating = sq.Column(sq.Float(), default=400.0)
    times = sq.Column(sq.Integer(), default=0)


class Vote(Base):
    __tablename__: str = 'votes'

    id = sq.Column(sq.Integer(), primary_key=True)
    uuid = sq.Column(sq.String(64), unique=True)
    win_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
    lose_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
    timestamp = sq.Column(sq.DateTime(), default=datetime.utcnow)

Base.metadata.create_all(engine)

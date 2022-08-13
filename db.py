from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from settings import config


# Creating a binding to a DB to work with a DB
engine = create_engine(config.alchemy_url)

# Session object
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class object for model class
Base = declarative_base()
Base.query = session.query_property()

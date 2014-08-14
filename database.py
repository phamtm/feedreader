import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from celery.signals import worker_init

# Database URI path
SQLALCHEMY_DATABASE_URI = 'postgresql://minhpham:mac@localhost/feedreader'

# Set up the connection
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)

# Flask dbsession #
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))

# Celery database session
cdb_session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=True,
                                          bind=engine))

# Set up declarative base
DeclarativeBase = declarative_base()
DeclarativeBase.query = db_session.query_property()


# Create all tables
def init_db():
    # Import all modules here that might define models so that they will
    # be registed properly on the metadata. Otherwise we will have to
    # import them first before calling init_db()
    from app.models import (User, Role, Connection, ViewHistory,
                            FeedArticle, FeedProvider, FeedSource,
                            FeedSubscription, FeedVote)
    DeclarativeBase.metadata.create_all(bind=engine)

# Drop all tables
def drop_db():
    DeclarativeBase.metadata.drop_all(bind=engine)


# Async dbsession #
###################
@worker_init.connect
def initialize_worker_session(signal, sender):
    new_engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
    cdb_session.configure(bind=new_engine)

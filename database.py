import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

class SQLAlchemy(object):

    def __init__(self):
        self.engine = None
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=True))
        # Set up declarative base
        self.Model = declarative_base()
        self.Model.query = self.session.query_property()

    def init_app(self, app):
        # if isinstance(app, Flask):
        # Set up the connection
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                                    convert_unicode=True)
        self.session.configure(bind=self.engine)

    def create_all(self):
        # Import all modules here that might define models so that they will
        # be registed properly on the metadata. Otherwise we will have to
        # import them first before calling create_all()
        from app.models import (User, Role, Connection, ViewHistory,
                                FeedArticle, FeedProvider, FeedSource,
                                FeedSubscription, FeedVote)
        self.Model.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.Model.metadata.drop_all(bind=self.engine)

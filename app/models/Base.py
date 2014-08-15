from app import db
from sqlalchemy import Column, Integer, DateTime, func

# Define a base table for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = Column(Integer, primary_key = True)
    date_created = Column(DateTime, default = func.current_timestamp())
    date_modified = Column(DateTime,
                           default = func.current_timestamp(),
                           onupdate = func.current_timestamp())

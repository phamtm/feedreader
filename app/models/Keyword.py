from sqlalchemy import (func, Column, Integer, Unicode, DateTime)

from app import db


class Keyword(db.Model):
    __tablename__ = 'keyword'

    keyword = Column(Unicode(128), convert_unicode=True, primary_key=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified= Column(DateTime, default=func.current_timestamp())

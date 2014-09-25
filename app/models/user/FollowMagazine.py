from sqlalchemy import (func, Column, DateTime, Integer,
                        ForeignKey, PrimaryKeyConstraint)
from sqlalchemy.orm import backref, relationship

from app import db


class FollowMagazine(db.Model):
    __tablename__ = 'followmagazine'

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'magazine_id'),
    )

    user_id = Column(Integer, ForeignKey('user.id'))
    magazine_id = Column(Integer, ForeignKey('magazine.id'))
    date_created = Column(DateTime, default=func.current_timestamp())
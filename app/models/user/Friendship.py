from sqlalchemy import (Column, DateTime, ForeignKey,
                        Integer, PrimaryKeyConstraint, func)
from sqlalchemy.orm import backref, relationship

from app import db


class Friendship(db.Model):

    __tablename__ = 'friendship'

    __table_args__ = (
        PrimaryKeyConstraint('user_id1', 'user_id2'),
    )

    user_id1 = Column(Integer, ForeignKey('user.id'))
    user_id2 = Column(Integer, ForeignKey('user.id'))
    date_created = Column(DateTime, default=func.current_timestamp())


    def __repr__(self):
        return '<Friendship (%d, %d)>' % (self.user_id1, self.user_id2)
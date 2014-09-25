from sqlalchemy import (Column, DateTime, ForeignKey,
                        Integer, PrimaryKeyConstraint, func)
from sqlalchemy.orm import backref, relationship

from app import db


class FollowUser(db.Model):

    __tablename__ = 'followuser'

    __table_args__ = (
        PrimaryKeyConstraint('user_id1', 'user_id2'),
    )

    user_id1 = Column(Integer, ForeignKey('user.id'))
    user_id2 = Column(Integer, ForeignKey('user.id'))
    date_created = Column(DateTime, default=func.current_timestamp())


    def __repr__(self):
        return '<FollowUser (%d, %d)>' % (self.user_id1, self.user_id2)
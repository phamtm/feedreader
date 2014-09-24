from sqlalchemy import (Column, Integer, ForeignKey)
from sqlalchemy.orm import backref, relationship

from app.models.Base import Base

class FollowMagazine(Base):
    __tablename__ = 'followmagazine'

    __tableargs__ = (
        UniqueConstraint('user_id', 'magazine_id'),
    )

    user_id = Column(Integer, ForeignKey('user.id'))
    magazine_id = Column(Integer, ForeignKey('magazine.id'))

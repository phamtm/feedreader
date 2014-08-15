from sqlalchemy import (Column, Integer, DateTime, ForeignKey,
						PrimaryKeyConstraint, func)

from app import db

class ViewHistory(db.Model):

	__tablename__ = 'viewhistory'
	__table_args__ = (
        PrimaryKeyConstraint('user_id', 'article_id'),
	)

	user_id = Column(Integer, ForeignKey('user.id'))
	article_id = Column(Integer, ForeignKey('feedarticle.id'))
	date_created = Column(DateTime, default=func.current_timestamp())

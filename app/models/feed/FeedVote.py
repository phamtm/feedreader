from sqlalchemy import (Column, Integer, Boolean, DateTime,
                        ForeignKey, PrimaryKeyConstraint, func)

from app import db

class FeedVote(db.Model):

    __tablename__ = 'feedvote'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'article_id'),
    )

    user_id = Column(Integer, ForeignKey('user.id'))
    article_id = Column(Integer, ForeignKey('feedarticle.id'))
    is_upvote = Column(Boolean, default=True)

    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime,
                           default=func.current_timestamp(),
                           onupdate=func.current_timestamp())


    def __repr__(self):
        return '<FeedVote article_id=%d, user_id=%s, is_upvote=%d>' \
                % (self.article_id, self.user_id, self.is_upvote)
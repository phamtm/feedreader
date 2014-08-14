from sqlalchemy import (Column, Integer, Unicode, UnicodeText, String,
                        Float, DateTime, ForeignKey, UniqueConstraint, func)
from sqlalchemy.orm import backref, relationship

from app.utils import wilson_score
from app.recommender.vnstemmer import vnstring_to_ascii
from app.models.Base import Base
from database import DeclarativeBase

class FeedArticle(Base):

    __tablename__ = 'feedarticle'

    __table_args__ = (
        UniqueConstraint('link', 'source_id'),
    )

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255, convert_unicode=True), nullable=False)
    link = Column(String(511))
    summary = Column(UnicodeText(convert_unicode=True))
    summary_ascii = Column(UnicodeText(convert_unicode=True))
    thumbnail_url = Column(String(511))
    time_published = Column(DateTime, default=func.current_timestamp())
    source_id = Column(Integer, ForeignKey('feedsource.id'))
    source = relationship('FeedSource', backref='article')

    # Related articles (csv)
    related_articles = Column(String(127), default='')

    # Readablility processed article
    readable_content = Column(UnicodeText(convert_unicode=True), nullable=True)

    # Vote records
    upvote = Column(Integer, default=0)
    downvote = Column(Integer, default=0)
    wilson_score = Column(Float, default=0.0)
    views = Column(Integer, default=0)


    def update_wilson_score(self):
        self.wilson_score = wilson_score(self.upvote, self.upvote + self.downvote)


    def get_related_articles(self):
        return map(int, self.related_articles.split())


    def __repr__(self):
        return '<FeedArticle %s %s>' % (self.title.encode('utf-8'), self.link.encode('utf-8'))

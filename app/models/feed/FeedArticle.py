# import flask.ext.whooshalchemy as whooshalchemy
from sqlalchemy import (Column, Integer, Unicode, UnicodeText, String,
                        Float, DateTime, ForeignKey, UniqueConstraint, func)
from sqlalchemy.orm import backref, relationship

from app import db
from app.models.Base import Base
from app.utils import wilson_score

class FeedArticle(Base):
    """An article
    :param int id: The identifier
    :param title: The unicode title
    :param summary:
    :param thumbnail_url:
    :param time_published:
    :param source_id:
    :param source:
    :param related_articles:
    :param html_readable:
    :param int upvote:
    :param int downvote:
    :param float wilson_score:
    :param int views:
    """

    __tablename__ = 'feedarticle'

    __table_args__ = (
        UniqueConstraint('link', 'source_id'),
    )

    __searchable__ = ['title']

    title = Column(Unicode(255, convert_unicode=True), nullable=False)
    link = Column(String(511))

    summary = Column(UnicodeText(convert_unicode=True))

    thumbnail_url = Column(String(511))

    time_published = Column(DateTime, default=func.current_timestamp())

    source_id = Column(Integer, ForeignKey('feedsource.id'))
    source = relationship('FeedSource', backref='articles')

    # Related articles (csv)
    related_articles = Column(String(127), default='')

    # Readablility processed article
    html = Column(UnicodeText(convert_unicode=True))
    # html_readable = Column(UnicodeText(convert_unicode=True))

    # Vote records
    upvote = Column(Integer, default=0)
    downvote = Column(Integer, default=0)
    wilson_score = Column(Float, default=0.0)
    views = Column(Integer, default=0)


    def update_wilson_score(self):
        self.wilson_score = wilson_score(self.upvote, self.upvote + self.downvote)


    def get_related_articles(self):
        return map(int, self.related_articles.split())


    def to_json(self):
        """Return JSON representation of the article"""
        return {
            'id':self.id,
            'link':self.link,
            'summary':self.summary,
            'title':self.title,
            'thumbnail_url':self.thumbnail_url,
            'upvote':self.upvote,
            'downvote':self.downvote,
            'views':self.views
        }


    def __repr__(self):
        return '<FeedArticle %s %s>' % (self.title.encode('utf-8'), self.link.encode('utf-8'))


# whooshalchemy.whoose_index(app, FeedArticle)
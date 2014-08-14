from urlparse import urlparse
from sqlalchemy import Column, String, Unicode, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.models.Base import Base

class FeedSource(Base):

    """
    name    : The name of this feed, eg: 'VnExpress.net - Kinh Doanh'
    _href   : The URL to the rss feed
    articles: List of articles in from the same source
    """

    __tablename__ = 'feedsource'

    name = Column(Unicode(255, convert_unicode=True), nullable=False)
    _url = Column(String(511), nullable=False)
    provider_id = Column(Integer, ForeignKey('feedprovider.id'))
    # articles = relationship('FeedArticle', backref='source', lazy='dynamic')
    # timestamp_format = Column(String(65), nullable=False)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        o = urlparse(url)
        if not o.path.endswith('.xml') and not o.path.endswith('.rss') and not o.path.endswith('rss/'):
            raise AttributeError('Invalid feed URL', url)
        self._url = url


    def __repr__(self):
        return '<FeedSource %s %s>' % (self.name.encode('utf-8'), self.url.encode('utf-8'))


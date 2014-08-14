from sqlalchemy import Column, Unicode, String
from sqlalchemy.orm import relationship, backref
from app.models.Base import Base
import re


class FeedProvider(Base):

    __tablename__ = 'feedprovider'

    name = Column(Unicode(255), nullable=False)
    _domain = Column(String(511), nullable=False)
    categories = relationship('FeedSource', backref='provider', lazy='dynamic')

    domain_regex = re.compile(r'^http://'
                                 r'([-a-zA-Z0-9]*\.)?'
                                 r'[-a-zA-Z0-9]+'
                                 r'\.[a-zA-Z]+'
                                 r'(:\d{0,7})?'
                                 r'/?')


    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, url):
        if not FeedProvider.domain_regex.match(url):
            raise AttributeError('Invalid RSS domain', url)
        self._domain = url

    def __repr__(self):
        return '<FeedProvider %s %s>' % (self.name.encode('utf-8'), self.domain.encode('utf-8'))


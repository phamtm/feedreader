from app import db
from Base import Base
import re



class FeedSource(Base):

	__tablename__ 	= 'feedsource'

	"""
	name 	: The name of this feed, eg: 'VnExpress.net - Kinh Doanh'
	_href 	: The URL to the rss feed
	articles: List of articles in from the same source
	"""
	name 			= db.Column(db.String(255), nullable = False)
	_href 			= db.Column(db.String(511), nullable = False)
	provider_id 	= db.Column(db.Integer, db.ForeignKey('feedprovider.id'))
	articles 		= db.relationship('FeedArticle', backref = 'source', lazy = 'dynamic')

	source_regex 	= re.compile(r'^http://'
								 r'([-a-zA-Z0-9]*\.)?'
								 r'[-a-zA-Z0-9]+'
							  	 r'\.[a-zA-Z]+'
							  	 r'(:\d{0,7})?'
							  	 r'/.+rss?')


	@property
	def href(self):
		return self._href

	@href.setter
	def href(self, url):
		if not FeedSource.source_regex.match(url):
			raise AttributeError('Invalid RSS URL', url)
		self._href = url


	def __repr__(self):
		return '<FeedSource %s %s>' % (self.name, self.href)


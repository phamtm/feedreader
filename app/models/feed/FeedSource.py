from app import db
from ..Base import Base
from urlparse import urlparse



class FeedSource(Base):

	__tablename__ 	= 'feedsource'

	"""
	name 	: The name of this feed, eg: 'VnExpress.net - Kinh Doanh'
	_href 	: The URL to the rss feed
	articles: List of articles in from the same source
	"""
	name 			= db.Column(db.Unicode(255, convert_unicode = True), nullable = False)
	_href 			= db.Column(db.String(511), nullable = False)
	provider_id 	= db.Column(db.Integer, db.ForeignKey('feedprovider.id'))
	articles 		= db.relationship('FeedArticle', backref = 'source', lazy = 'dynamic')
	# timestamp_format = db.Column(db.String(65), nullable = False)

	@property
	def href(self):
		return self._href

	@href.setter
	def href(self, url):
		o = urlparse(url)
		if not o.path.endswith('.xml') and not o.path.endswith('.rss'):
			raise AttributeError('Invalid feed URL', url)
		self._href = url


	def __repr__(self):
		return '<FeedSource %s %s>' % (self.name.encode('utf-8'), self.href.encode('utf-8'))


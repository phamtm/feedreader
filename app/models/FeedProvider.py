from app import db
from Base import Base
import re



class FeedProvider(Base):

	__tablename__ 	= 'feedprovider'

	name 			= db.Column(db.String(255), nullable = False)
	_domain 		= db.Column(db.String(511), nullable = False)
	categories 		= db.relationship('FeedSource', backref = 'provider', lazy = 'dynamic')

	domain_regex 	= re.compile(r'^http://'
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
		return '<FeedProvider %s %s>' % (self.name, self.domain)


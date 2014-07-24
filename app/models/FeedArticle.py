from app import db
from Base import Base



class FeedArticle(Base):

	__tablename__ 		= 'feedarticle'
	title 				= db.Column(db.Unicode(255, convert_unicode = True), nullable = False)
	link 				= db.Column(db.String(511), nullable = False)
	summary				= db.Column(db.UnicodeText(convert_unicode = True))
	image_url 			= db.Column(db.String(511))
	time_published		= db.Column(db.DateTime)

	source_id 			= db.Column(db.Integer, db.ForeignKey('feedsource.id'))

	db.UniqueConstraint('link', 'source_id')


	def __repr__(self):
		return '<FeedArticle %s %s>' % (self.title.encode('utf-8'), self.link.encode('utf-8'))


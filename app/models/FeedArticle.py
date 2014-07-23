from app import db
from Base import Base



class FeedArticle(Base):

	__tablename__ 		= 'feedarticle'
	title 				= db.Column(db.String(255), nullable = False)
	link 				= db.Column(db.String(511), nullable = False, unique = True)
	image_url 			= db.Column(db.String(511))
	time_published		= db.Column(db.DateTime)
	provider_article_id = db.Column(db.String(511), nullable = False)

	source_id 			= db.Column(db.Integer, db.ForeignKey('feedsource.id'))


	def __repr__(self):
		return '<FeedArticle %s %s>' % (self.title, self.link)


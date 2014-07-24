from app import db



class FeedArticle(db.Model):

	__tablename__ 		= 'feedarticle'

	__table_args__		= (
			db.PrimaryKeyConstraint('link', 'source_id'),
		)

	title 				= db.Column(db.Unicode(255, convert_unicode = True), nullable = False)
	link 				= db.Column(db.String(511))
	summary				= db.Column(db.UnicodeText(convert_unicode = True))
	image_url 			= db.Column(db.String(511))
	time_published		= db.Column(db.DateTime)

	date_created 	= db.Column(db.DateTime, default = db.func.current_timestamp())
	date_modified 	= db.Column(db.DateTime,
							  default = db.func.current_timestamp(),
							  onupdate = db.func.current_timestamp())

	source_id 			= db.Column(db.Integer, db.ForeignKey('feedsource.id'))



	def __repr__(self):
		return '<FeedArticle %s %s>' % (self.title.encode('utf-8'), self.link.encode('utf-8'))


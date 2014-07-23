from app import db



class FeedSubscription(db.Model):

	__tablename__ 	= 'feedsubscription'

	id 				= db.Column(db.Integer, primary_key = True)
	user_id 		= db.Column(db.Integer, db.ForeignKey('user.id'))
	source_id 		= db.Column(db.Integer, db.ForeignKey('feedsource.id'))


	def __repr__(self):
		return '<Subscription user_id =%d, source_id=%d>' % (self.user_id, self.source_id)
from app import db


class Connection(db.Model):

	__tablename__ 		= 'connection'

	__table_args__		= (
			db.UniqueConstraint('user_id', 'provider_id'),
		)

	id 					= db.Column(db.Integer, primary_key = True)
	user_id 			= db.Column(db.Integer, db.ForeignKey('user.id'))

	# Provider details
	provider_id 		= db.Column(db.Integer, nullable = False)
	provider_user_id 	= db.Column(db.String(255))

	# Access tokens
	oauth_token 		= db.Column(db.String(255))
	oauth_secret 		= db.Column(db.String(255))

	# Social profile
	display_name 		= db.Column(db.String(255), nullable = False)
	image_url 			= db.Column(db.String(255))


	def __repr__(self):
		return '<provider_id = %s, provider_user_id = %s, display_name = %s>' % \
				(self.provider_id, self.provider_user_id, self.display_name)


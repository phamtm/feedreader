from app import db
from Permission import roles



class Role(db.Model):
	__tablename__ 	= 'role'
	id 				= db.Column(db.Integer, primary_key = True)
	name 			= db.Column(db.String(64), unique = True)
	permissions		= db.Column(db.Integer)
	default			= db.Column(db.Boolean, default = False)
	user			= db.relationship('User', backref = 'role', lazy = 'dynamic')


	def __repr__(self):
		return '<Role %r %r %r>' % (self.name, self.permissions, self.default)


	@staticmethod
	def insert_roles():
		for r in roles:
			role = Role.query.filter_by(name = r).first()
			if role is None:
				role = Role(name = r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

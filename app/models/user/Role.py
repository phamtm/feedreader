from app import db
from Permission import roles



class Role(db.Model):
    """User's role in the application
    :param int id: Id of the role
    :param str name: Name of the role
    :param int permissions: The permissions flag for this user
    :param bool default:
    :param user: List of users having this role
    """

    __tablename__   = 'role'
    id              = db.Column(db.Integer, primary_key = True)
    name            = db.Column(db.String(64), unique = True)
    permissions     = db.Column(db.Integer)
    default         = db.Column(db.Boolean, default = False)
    users           = db.relationship('User', backref = 'role', lazy = 'dynamic')


    def __repr__(self):
        return '<Role %r %r %r>' % (self.name, self.permissions, self.default)


    @staticmethod
    def insert_roles():
        """Insert roles into the database"""
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if not role:
                role = Role(name = r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

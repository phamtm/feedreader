from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import backref, relationship

from app import db
from app.models.user.Permission import roles


class Role(db.Model):
    """User's role in the application
    :param int id: Id of the role
    :param str name: Name of the role
    :param int permissions: The permissions flag for this user
    :param bool default:
    :param user: List of users having this role
    """

    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    permissions = Column(Integer)
    default = Column(Boolean, default=False)
    users = relationship('User', backref='role', lazy='dynamic')


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

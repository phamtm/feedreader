from werkzeug.security import generate_password_hash, check_password_hash
# Generate secure JSON Web Signature with a time expiration
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# Default class that implements required methods for User model
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import db
from app import login_manager
from app.models.Base import Base
from app.models.feed import FeedSource, FeedSubscription
from app.models.user.Role import Role

"""
.. module:: User
    :sypnosis: The user of the website
"""


class User(UserMixin, Base):
    """The user of the website
    :param str name: The name of the user
    :param str email: Unique email address for the user
    :param str password_hash: The hash of user's password
    :param bool confirmed: Has the user confirmed the email address?
    :param int role_id: The id for the role of user
    :param bool register_with_provider: Is the user registered through a social account
    :param connections: List of socials account connected with this user
    :param feed_subscriptions: List of user's feed subscriptions
    """

    __tablename__ = 'user'

    # User name
    name = Column(String(63), default='User')

    # Authentication data
    email = Column(String(127), nullable=False, unique=True, index=True)
    password_hash = Column(String(127))
    confirmed = Column(Boolean, default=False)
    role_id= Column(Integer, ForeignKey('role.id'))
    register_with_provider = Column(Boolean, default=False)

    # Social login connection
    connections = relationship('Connection', backref = 'user', lazy = 'dynamic')

    # Subscription to feed sources
    feed_subscriptions = relationship('FeedSubscription', backref = 'user', lazy = 'dynamic')


    # Initilization of user's role
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if not self.role:
            # If the email is the same as admin's email, assign admin role
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions = 0xff).first()
            else:
                self.role = Role.query.filter_by(default = True).first()


    # Create a set only password property that create a hash
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    # Check if password can generate password_hash
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # Generate a token used for account activation
    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        token = s.dumps({'confirm_id': self.id})
        return token


    # Generate a token used for account activation
    def generate_reset_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        token = s.dumps({'reset_id': self.id})
        return token


    # Confirm the token and activate the account
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return False

        # Disallow users to activate somebody else's account even if have their
        # token
        if data['confirm_id'] != self.id:
            return False

        self.confirmed = True
        db.session.add(self)

        return True


    # Check if the user has permission
    def has_permissions(self, perm):
        return self.role and                            \
               (perm & self.role.permissions) == perm


    # Subscribe to a feed source
    def subscribe_feed(self, source_id):
        source = FeedSource.query.get(source_id)
        if source and not self.is_subscribed(source_id):
            sub = FeedSubscription(user_id = self.id, source_id = source_id)
            db.session.add(sub)
            db.session.commit()


    # Unsubscribe a feed source
    def unsubscribe_feed(self, source_id):
        sub = FeedSubscription.query.filter_by(user_id = self.id, source_id = source_id).first()
        if sub:
            db.session.delete(sub)
            db.session.commit()


    # Test if the user subscribed to a feed source
    def is_subscribed(self, source_id):
        sub = FeedSubscription.query.filter_by(user_id = self.id, source_id = source_id).first()
        return sub


    def __repr__(self):
        return '<user %r %r>' % (self.id, self.email)



class AnonymousUser(AnonymousUserMixin):
    def has_permissions(self, perm):
        return False


# A callback to load user by id required by login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
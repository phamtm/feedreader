from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager
from app.models.Base import Base
from app.models.feed import FeedSource, FeedSubscription
from app.models.user import FollowUser, FollowMagazine, Friendship, Role

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
    connections = relationship('Connection', backref='user', lazy='dynamic')

    # Subscription to feed sources
    feed_subscriptions = relationship('FeedSubscription',
                                      backref='user',
                                      lazy='dynamic')
    magazines = relationship('Magazine', backref='user', lazy='dynamic')


    # Initilization of user's role
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if not self.role:
            # If the email is the same as admin's email, assign admin role
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            else:
                self.role = Role.query.filter_by(default = True).first()


    @property
    def password(self):
        """Create a set only password property that create a hash"""
        raise AttributeError("Password is not a readable attribute")


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        """Check if password can generate password_hash"""
        return check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self, expiration=3600):
        """Generate a token used for account activation"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'confirm_id': self.id})
        return token


    def generate_reset_token(self, expiration=3600):
        """Generate a token used for account activation"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'reset_id': self.id})
        return token


    def generate_auth_token(self, expiration=3600):
        """Generate a token used for API access."""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'auth_id': self.id})
        return token


    @staticmethod
    def verify_auth_token(token):
        """Verify the authentication token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['auth_id'])


    def confirm(self, token):
        """Confirm the token and activate the account"""
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


    def has_permissions(self, perm):
        """Check if the user has permission"""
        return self.role and                            \
               (perm & self.role.permissions) == perm


    def subscribe_feed(self, source_id):
        """Subscribe to a feed source"""
        source = FeedSource.query.get(source_id)
        if source and not self.is_subscribed(source_id):
            sub = FeedSubscription(user_id = self.id, source_id = source_id)
            db.session.add(sub)
            db.session.commit()


    def unsubscribe_feed(self, source_id):
        """Unsubscribe a feed source"""
        sub = FeedSubscription.query.filter_by(user_id = self.id, source_id = source_id).first()
        if sub:
            db.session.delete(sub)
            db.session.commit()


    def is_subscribed(self, source_id):
        """Test if the user subscribed to a feed source"""
        sub = FeedSubscription.query.filter_by(user_id = self.id, source_id = source_id).first()
        return sub is not None


    def own_magazine(self, magazine_id):
        """Test if the user own a magazine"""
        magazine = Magazine.query.filter_by(magazine_id=magazine_id,
                                            user_id=self.id)
        return magazine is not None


    def get_subscriptions(self):
        """Return a list of the user's subscriptions"""
        subs = FeedSource.query               \
            .join(                                                  \
                FeedSubscription,                                   \
                FeedSubscription.source_id == FeedSource.id)        \
            .filter_by(user_id=self.id)                             \
            .order_by(FeedSource.name.asc()).all()

        return subs


    def add_friend(self, friend_id):
        """Add friendship between two people"""
        if not User.query.get(friend_id):
            return

        friendship = Friendship.query.get((self.id, friend_id))
        following = FollowUser.query.get((self.id, friend_id))

        if not friendship:
            friendship1 = Friendship(user_id1=self.id, user_id2=friend_id)
            friendship2 = Friendship(user_id1=friend_id, user_id2=self.id)
            if following:
                db.session.delete(following)
            db.session.add_all([friendship1, friendship2])
            db.session.commit()


    def remove_friend(self, friend_id):
        """Remove friendship between two people"""
        friendship1 = Friendship.query.get((self.id, friend_id))
        friendship2 = Friendship.query.get((friend_id, self.id))

        if friendship1 and friendship2:
            db.session.delete(friendship1)
            db.session.delete(friendship2)
            db.session.commit()


    def follow_user(self, user_id):
        """Folow a user. You are not the friend with the followee"""
        following = FollowUser.query.get((self.id, user_id))
        friendship = Friendship.query.get((self.id, user_id))
        if not following and not friendship:
            follow_user = FollowUser(user_id1=self.id, user_id2=user_id)
            db.session.add(follow_user)
            db.session.commit()


    def unfollow_user(self, user_id):
        """Unfolow a user"""
        follow_user = FollowUser.query.get((self.id, user_id))
        db.session.delete(follow_user)
        db.session.commit()


    def follow_magazine(self, magazine_id):
        """Follow a magazine"""
        magazine = Magazine.query.get(magazine_id)
        follow_magazine = FollowMagazine.query.get((self.id, magazine_id))
        if magazine.public and not follow_magazine:
            follow_magazine = FollowMagazine(user_id=self.id,
                                             magazine_id=magazine_id)
            db.session.add(follow_magazine)
            db.session.commit()


    def unfollow_magazine(self, magazine_id):
        """Unfollow a magazine"""
        follow_magazine = FollowMagazine.query.get((self.id, magazine_id))
        if follow_magazine:
            db.session.delete(follow_magazine)
            db.session.commit()



    def __repr__(self):
        return '<user %r %r>' % (self.id, self.email)



class AnonymousUser(AnonymousUserMixin):
    def has_permissions(self, perm):
        return False


# A callback to load user by id required by login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
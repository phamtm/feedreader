from User import User, AnonymousUser
from Role import Role
from FeedArticle import FeedArticle
from FeedSource import FeedSource
from FeedSubscription import FeedSubscription
from FeedProvider import FeedProvider
from Connection import Connection
from Permission import Permission

from app import login_manager


login_manager.anonymous_user = AnonymousUser

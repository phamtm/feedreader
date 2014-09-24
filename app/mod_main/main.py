from app.mod_main import mod_main
from app.models import FeedSource, FeedSubscription

def before_request():
    subs = FeedSource.query                                     \
        .join(
            FeedSubscription,
            FeedSubscription.source_id == FeedSource.id)        \
        .filter_by(user_id=current_user.id)                     \
        .order_by(FeedSource.name.asc())

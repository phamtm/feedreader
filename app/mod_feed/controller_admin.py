from app.mod_feed import mod_feed
from app.decorators import permission_required
from app.models import Permission
from app.models imort FeedAggregator


@mod_feed.route('/updatedb')
@permission_required(Permission.ADMIN)
def update_feeds_db():
	fa = FeedAggregator()
	fa.update_feed_db()
	return 'updating feeds db'

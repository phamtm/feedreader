from flask import url_for, 					\
				  render_template,			\
				  session,					\
				  redirect,					\
				  flash,					\
				  request
from flask.ext.login import login_required,	\
							current_user

from app.mod_feed import mod_feed
from app.mod_feed.sources import feed_sources
from app.mod_feed.FeedAggregator import FeedAggregator
from app.models import FeedSource, 			\
					   Permission
from app.utils import Future
from app.decorators import permission_required

import feedparser


@mod_feed.route('/all')
def all_feeds():
	entries = get_all_rss_feeds()
	return render_template('feeds.html', rss_entries = entries)


@mod_feed.route('/subscriptions')
@login_required
def manage_subscriptions():
	hit_list = [{
			'id': source.id,
			'name': source.name,
			'href': source.href,
			'subscribed': False
		} for source in FeedSource.query.all()]

	return render_template('feed_sources.html', rss_sources = hit_list)


@mod_feed.route('/subscribe')
@login_required
def subscribe_feed():
	source_id = request.args.get('source_id')
	if source_id is not None:
		current_user.subscribe_feed(source_id)
		flash('Subscribe successful to source=%s' % source_id)

	return redirect(url_for('mod_feed.manage_subscriptions'))


@mod_feed.route('/unsubscribe')
@login_required
def unsubscribe_feed():
	source_id = request.args.get('source_id')
	if source_id is not None:
		current_user.unsubscribe_feed(source_id)
		flash('Unsubscribe successful source=%s' % source_id)

	return redirect(url_for('mod_feed.manage_subscriptions'))


@mod_feed.route('/updatedb')
@permission_required(Permission.ADMIN)
def update_feeds_db():
	fa = FeedAggregator()
	fa.get_all_feeds()
	return 'updating feeds db'




def get_all_rss_feeds():
	hit_list = [source.href for source in FeedSource.query.all()]

	# Send out multiple request at once
	future_calls = [Future(feedparser.parse, rss_url) for rss_url in hit_list]
	feeds = [future_obj() for future_obj in future_calls]

	# Extract all entries
	entries = []
	for feed in feeds:
		entries.extend(feed['entries'])

	return entries


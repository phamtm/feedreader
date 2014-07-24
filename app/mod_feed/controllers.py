from flask import url_for, 						\
				  render_template,				\
				  session,						\
				  redirect,						\
				  flash,						\
				  request
from flask.ext.login import login_required,		\
							current_user

from app import db
from app.mod_feed import mod_feed
from app.mod_feed.sources import feed_sources
from app.models import FeedSource, 				\
					   FeedArticle,				\
					   FeedSubscription,		\
					   Permission
from app.utils import Future
from app.decorators import permission_required

import feedparser


@mod_feed.route('/all')
@login_required
def all_feeds():
	articles = FeedArticle.query 	\
		.join(FeedSubscription, FeedSubscription.source_id == FeedArticle.source_id)	\
		.filter_by(user_id = current_user.id)	\
		.all()

	return render_template('feeds.html', rss_articles = articles)


@mod_feed.route('/subscriptions')
@login_required
def manage_subscriptions():
	hit_list = [{
			'id': source.id,
			'name': source.name,
			'href': source.href,
			'subscribed': False
		} for source in FeedSource.query.all()]

	subscribed_sources = FeedSource.query	\
					.outerjoin(FeedSubscription, FeedSource.id == FeedSubscription.source_id)	\
					.filter_by(user_id = current_user.id)	\
					.all()

	not_subscribed_sources = FeedSource.query	\
					.outerjoin(FeedSubscription, FeedSource.id == FeedSubscription.source_id)	\
					.filter_by(user_id = None)	\
					.all()

	return render_template('feed_sources.html',
							subscribed = subscribed_sources,
							not_subscribed = not_subscribed_sources)


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
	return 'updating feeds db'


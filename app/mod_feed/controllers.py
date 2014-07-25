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
from FeedAggregator import FeedAggregator
from app.mod_feed.sources import feed_sources
from app.models import FeedSource, 				\
					   FeedArticle,				\
					   FeedSubscription,		\
					   FeedVote,				\
					   Permission
from app.utils import Future
from app.decorators import permission_required

import feedparser


@mod_feed.route('/public/all')
def all_public_feed():
	return 'all public feed'


@mod_feed.route('/all')
@mod_feed.route('/index')
@login_required
def all_feeds():
	articles = FeedArticle.query 	\
		.join(FeedSubscription, FeedSubscription.source_id == FeedArticle.source_id)	\
		.filter_by(user_id = current_user.id)	\
		.order_by(FeedArticle.wilson_score.desc())		\
		.all()

	return render_template('feeds.html', rss_articles = articles)


@mod_feed.route('/source')
@login_required
def feeds_from_source():
	source_id = request.args.get('source_id')

	if source_id is None or not current_user.is_subscribed(source_id):
		abort(404)

	rss_articles = FeedArticle.query.filter_by(source_id = source_id)

	return render_template('feeds.html', rss_articles = articles)


@mod_feed.route('/subscriptions')
@login_required
def manage_subscriptions():
	subscribed_sources = FeedSource.query	\
					.outerjoin(FeedSubscription, FeedSource.id == FeedSubscription.source_id)	\
					.filter_by(user_id = current_user.id)	\
					.all()

	not_subscribed_sources = FeedSource.query	\
					.outerjoin(FeedSubscription, FeedSource.id == FeedSubscription.source_id)	\
					.filter(db.or_(FeedSubscription.user_id == None,
						FeedSubscription.user_id < current_user.id,
						FeedSubscription.user_id > current_user.id))	\
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


@mod_feed.route('/upvote')
@login_required
def upvote():
	article_id = request.args.get('article_id')

	if article_id is None:
		return redirect(url_for('mod_main.all_feeds'))

	article = FeedArticle.query.get(article_id)

	# Article does not exist
	if article is None:
		abort(404)

	vote = FeedVote.query.filter_by(user_id = current_user.id, article_id = article_id).first()

	# No vote from the user yet, add one
	if vote is None:
		vote = FeedVote(user_id = current_user.id, article_id = article_id, is_upvote = True)
		article.upvote += 1
		article.update_wilson_score()
		db.session.add(vote)
	else:
		if not vote.is_upvote:
			vote.is_upvote = True
			article.upvote += 1
			article.downvote -= 1
			article.update_wilson_score()

	return redirect(url_for('mod_feed.all_feeds'))


@mod_feed.route('/downvote')
@login_required
def downvote():
	article_id = request.args.get('article_id')

	if article_id is None:
		return redirect(url_for('mod_main.all_feeds'))

	article = FeedArticle.query.get(article_id)

	# Article does not exist
	if article is None:
		abort(404)

	vote = FeedVote.query.filter_by(user_id = current_user.id, article_id = article_id).first()

	# No vote from the user yet, add one
	if vote is None:
		vote = FeedVote(user_id = current_user.id, article_id = article_id, is_upvote = False)
		article.downvote += 1
		article.update_wilson_score()
		db.session.add(vote)
	else:
		if vote.is_upvote:
			vote.is_upvote = False
			article.upvote -= 1
			article.downvote += 1
			article.update_wilson_score()

	return redirect(url_for('mod_feed.all_feeds'))


@mod_feed.route('/remove_vote')
@login_required
def remove_vote():
	article_id = request.args.get('article_id')

	if article_id is None:
		return redirect(url_for('mod_main.all_feeds'))

	article = FeedArticle.query.get(article_id)

	# Article does not exist
	if article is None:
		abort(404)

	if article is not None:
		vote = FeedVote.query.filter_by(user_id = current_user.id, article_id = article_id).first()
		if vote is not None:
			if vote.is_upvote:
				article.upvote -= 1
			else:
				article.downvote -= 1
			article.update_wilson_score()
			db.session.delete(vote)

	return redirect(url_for('mod_feed.all_feeds'))

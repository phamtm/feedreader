from flask import (render_template,
                   current_app,
                   request,
                   abort)
from flask.ext.login import login_required, current_user

from app.mod_main import mod_main
from app.mod_feed import mod_feed
from app.models import FeedArticle, FeedSubscription, FeedSource
from Pagination import Pagination


@mod_main.route('/all')
@mod_feed.route('/all')
@login_required
def index():
    """Return all the feed articles from the user's subscription."""

    page = request.args.get('page', 1, type=int)

    start_idx = current_app.config['ARTICLES_PER_PAGE'] * (page - 1)
    stop_idx = start_idx + current_app.config['ARTICLES_PER_PAGE']

    rss_articles = FeedArticle.query                                \
        .join(
            FeedSubscription,
            FeedSubscription.source_id == FeedArticle.source_id)    \
        .filter_by(user_id=current_user.id)                         \
        .order_by(
            FeedArticle.wilson_score.desc(),
            FeedArticle.views.desc(),
            FeedArticle.time_published.desc())                      \
        .slice(start_idx, stop_idx)                                 \
        .all()

    count = FeedArticle.query                                       \
        .join(
            FeedSubscription,
            FeedSubscription.source_id == FeedArticle.source_id)    \
        .filter_by(user_id=current_user.id)                         \
        .order_by(
            FeedArticle.wilson_score.desc(),
            FeedArticle.views.desc(),
            FeedArticle.time_published.desc()).count()

    popular_articles = get_popular_articles()

    # error_out=False
    pagination = Pagination(
        page=page,
        per_page=current_app.config['ARTICLES_PER_PAGE'],
        total_count=count)

    return render_template(
        'feeds.html',
        rss_articles=rss_articles,
        popular_articles=popular_articles,
        pagination=pagination)


@mod_main.route('/')
@mod_feed.route('/')
@login_required
def feeds_from_source():
    """Return all articles from a source that the user subscribed to."""
    source_id = request.args.get('source_id', type=int)
    popular_articles = get_popular_articles()

    if not source_id or not current_user.is_subscribed(source_id):
        return render_template('feeds.html',
                               popular_articles=popular_articles)

    rss_articles = FeedArticle.query.                   \
        filter_by(source_id=source_id)                  \
        .order_by(FeedArticle.time_published.desc())    \
        .limit(30)


    return render_template(
        'feeds.html',
        source = FeedSource.query.get(source_id),
        rss_articles=rss_articles,
        popular_articles=popular_articles)


def get_popular_articles():
    articles = FeedArticle.query                    \
        .order_by(
            FeedArticle.wilson_score.desc(),
            FeedArticle.views.desc(),
            FeedArticle.time_published.desc())      \
        .limit(10).all()

    return articles


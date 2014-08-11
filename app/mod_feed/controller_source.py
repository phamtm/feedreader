from app.mod_main import mod_main
from app.mod_feed import mod_feed
from app.models import FeedArticle, FeedSubscription

from flask import (render_template,
                   current_app,
                   request,
                   abort)
from flask.ext.login import (login_required,
                             current_user)


@mod_main.route('/')
@mod_feed.route('/index')
@login_required
def index():
    """Return all the feed articles from the user's subscription."""

    page = request.args.get('page', 1, type=int)

    pagination = FeedArticle.query                                  \
        .join(
            FeedSubscription,
            FeedSubscription.source_id == FeedArticle.source_id)    \
        .filter_by(user_id=current_user.id)                         \
        .order_by(
            FeedArticle.wilson_score.desc(),
            FeedArticle.views.desc(),
            FeedArticle.time_published.desc())                      \
        .paginate(page,
                  per_page=current_app.config['ARTICLES_PER_PAGE'],
                  error_out=False)

    return render_template(
        'feeds.html',
        rss_articles=pagination.items,
        pagination=pagination)


@mod_feed.route('/source')
@login_required
def feeds_from_source():
    """Return all articles from a source that the user subscribed to."""

    source_id = request.args.get('source_id')

    if not source_id or not current_user.is_subscribed(source_id):
        abort(404)

    rss_articles = FeedArticle.query.filter_by(source_id=source_id)

    return render_template(
        'feeds.html',
        rss_articles=rss_articles)

from flask import (render_template,
                   request,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import login_required, current_user
from sqlalchemy import or_

from app import db
from app.mod_feed import mod_feed
from app.mod_auth.controller_login import load_subscriptions
from app.models import FeedSource, FeedSubscription


@mod_feed.route('/subscriptions')
@login_required
def manage_subscriptions():
    """Add/remove subscriptions."""

    subscribed_sources = FeedSource.query                                   \
                    .outerjoin(
                        FeedSubscription,
                        FeedSource.id == FeedSubscription.source_id)        \
                    .filter_by(
                        user_id=current_user.id)                            \
                    .all()

    not_subscribed_sources = FeedSource.query                               \
                    .outerjoin(
                        FeedSubscription,
                        FeedSource.id == FeedSubscription.source_id)        \
                    .filter(
                        or_(
                            FeedSubscription.user_id == None,
                            FeedSubscription.user_id < current_user.id,
                            FeedSubscription.user_id > current_user.id))    \
                    .all()

    return render_template('feed_sources.html',
                           subscribed=subscribed_sources,
                           not_subscribed=not_subscribed_sources)


@mod_feed.route('/subscribe')
@login_required
def subscribe_feed():
    """Subscribe to a feed."""

    source_id = request.args.get('source_id')
    if source_id:
        current_user.subscribe_feed(source_id)
        load_subscriptions()
        flash('Subscribe successful to source=%s' % source_id)

    return redirect(url_for('mod_feed.manage_subscriptions'))


@mod_feed.route('/unsubscribe')
@login_required
def unsubscribe_feed():
    """Unsubscribe from a feed."""

    source_id = request.args.get('source_id')
    if source_id:
        current_user.unsubscribe_feed(source_id)
        load_subscriptions()
        flash('Unsubscribe successful source=%s' % source_id)

    return redirect(url_for('mod_feed.manage_subscriptions'))

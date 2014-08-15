from flask import (url_for,
                   request,
                   session,
                   flash,
                   redirect)
from flask.ext.login import login_user

from app import db
from app.mod_auth import mod_auth
from app.decorators import unauthenticated_required
from app.models import User, Connection
from app.mod_auth.providers import provider_id
from app.mod_auth.controller_login import load_subscriptions
from app.mod_auth.providers import facebook


@mod_auth.route('/login/facebook')
@unauthenticated_required
def facebook_login():
    """Request for Facebook authorization."""
    next_url = request.args.get('next') or url_for('mod_feed.index')
    callback = url_for('mod_auth.facebook_authorized',
                       next=next_url,
                       _external=True)

    return facebook.authorize(callback=callback)


@mod_auth.route('/authorized/facebook')
@facebook.authorized_handler
def facebook_authorized(response):
    """Authorize the Facebook account.
    :param response: The response from Facebook
    """

    next_url = request.args.get('next') or url_for('mod_feed.index')

    if not response:
        flash('You denied the request to sign in')
        return redirect(next_url)

    # Store the token so we can access it later from tokengetter
    session['facebook_access_token'] = (response['access_token'], '')

    fbme = facebook.get('/me')
    email = fbme.data['email']

    # If the user is not registered, add him
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, register_with_provider=True)
        db.session.add(user)
        db.session.commit()

    # In any case we update the authentication token in the db
    # If the user has revoked access we will have new token here
    connection = Connection.query.filter_by(
        user_id=user.id,
        provider_id=provider_id['FACEBOOK']).first()

    if not connection:
        connection = Connection(
            user_id=user.id,
            provider_id=provider_id['FACEBOOK'],
            provider_user_id=fbme.data['id'],
            display_name=fbme.data['name'],
            image_url='https://graph.facebook.com/%s/picture?type=large' % \
                (fbme.data['id']),
            user=user)
        db.session.add(connection)

    connection.oauth_token = response['access_token']

    login_user(user)
    load_subscriptions()

    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    """Acquire the facebook token from session."""

    return session.get('facebook_access_token')

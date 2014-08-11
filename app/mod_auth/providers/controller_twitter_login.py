from flask import url_for,                  \
                  redirect,                 \
                  render_template,          \
                  request,                  \
                  flash,                    \
                  session

from flask.ext.login import current_user,   \
                            login_user

from app import db,                         \
                twitter
from app.models import User,                \
                       Connection
from app.mod_auth import mod_auth
from app.decorators import unauthenticated_required
from app.mod_auth.providers import provider_id


@mod_auth.route('/login/twitter')
@unauthenticated_required
def twitter_login():
    if session.has_key('twitter_oauth_token'):
        del session['twitter_oauth_token']
    return twitter.authorize(callback = url_for('mod_auth.twitter_authorized',
            next = request.args.get('next') or request.referrer or None))


@mod_auth.route('/authorized/twitter')
@twitter.authorized_handler
def twitter_authorized(response):
    next_url = request.args.get('next') or url_for('mod_feed.index')

    if not response:
        flash('You denied the request to sign in')
        return redirect(next_url)


    # Store the token so we can access it later from tokengetter
    session['twitter_oauth_token'] = (
            response['oauth_token'],
            response['oauth_token_secret']
        )

    twitter_user_id = response['user_id']
    twitter_screen_name = response['screen_name']

    resp = twitter.get('users/show.json', data = {'screen_name': twitter_screen_name})

    twitter_profile_image_url = resp.data['profile_image_url']

    # If the user is not registered, add him
    user = User.query.filter_by(email = twitter_screen_name).first()
    if not user:
        user = User(email = twitter_screen_name, register_with_provider = True)
        db.session.add(user)
        db.session.commit()

    # In any case we update the authentication token in the db
    # If the user has revoked access we will have new token here
    connection = Connection.query.filter_by(
        user_id = user.id,
        provider_id = provider_id['TWITTER']).first()

    if not connection:
        connection = Connection(
                user_id = user.id,
                provider_id = provider_id['TWITTER'],
                provider_user_id = twitter_user_id,
                display_name = twitter_screen_name,
                image_url = twitter_profile_image_url ,
                user = user
            )

    connection.oauth_token = response['oauth_token'],
    connection.oauth_secret = response['oauth_token_secret'],
    db.session.add(connection)

    login_user(user)

    flash('Logged in as id = %s, name = %s, redirect = %s, image_url = %s'  %   \
            (connection.provider_user_id, connection.display_name, twitter_profile_image_url, request.args.get('next')))

    return redirect(next_url)


@twitter.tokengetter
def get_twitter_oauth_token():
    return session.get('twitter_oauth_token')

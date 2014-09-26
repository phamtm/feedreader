from urllib2 import Request, urlopen, URLError
from flask import (url_for,
                   redirect,
                   url_for,
                   request,
                   flash,
                   session,
                   json)
from flask.ext.login import login_user

from app import db
from app.mod_auth.providers import provider_id
from app.mod_auth import mod_auth
from app.decorators import unauthenticated_required
from app.models import User, Connection, Magazine
from app.mod_auth.providers import google


@mod_auth.route('/login/google')
@unauthenticated_required
def google_login():
    """Request for Google account authorization."""

    session['google_auth_next_url'] = request.referrer or           \
                                      url_for('mod_feed.index') or  \
                                      request.args.get('next')


    callback = url_for('mod_auth.google_authorized', _external=True)
    return google.authorize(callback=callback)


@mod_auth.route('/authorized/google')
@google.authorized_handler
def google_authorized(response):
    """Authorize the Google account
    :param response: The response from Google's authorization service
    """

    access_token = response['access_token']
    session['google_token'] = (access_token, '')

    headers = {'Authorization': 'OAuth '+ access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)

    try:
        res = urlopen(req)
    except URLError as err:
        if err.code == 401:
            # Unauthorized - bad token
            session.pop('google_token', None)
            flash('You denied the request to sign in')
            return redirect(url_for('mod_auth.login'))

        flash('Something bad happened when signing with Google')
        return redirect(url_for('mod_auth.login'))

    user_info = json.loads(res.read())


    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(email=user_info['email'],
                    register_with_provider=True,
                    confirmed=True)
        db.session.add(user)
        db.session.commit()

    connection = Connection.query.filter_by(
        user_id=user.id,
        provider_id=provider_id['GOOGLE']).first()

    if not connection:
        connection = Connection(
            user_id=user.id,
            provider_id=provider_id['GOOGLE'],
            provider_user_id=user_info['id'],
            display_name=user_info['name'],
            image_url=user_info['picture'],
            user=user)

    connection.oauth_token = access_token
    db.session.add(connection)

    # Create a `Saved` magazine
    if not Magazine.query.filter_by(name='Saved').first():
        magazine = Magazine(name='Saved', public=False, user_id=user.id)
        db.session.add(magazine)
        db.session.commit()
        user.saved_magazine = magazine.id

    login_user(user)

    return redirect(session.get('google_auth_next_url'))


@google.tokengetter
def get_google_oauth_token():
    """Acquire the google token stored in session."""

    return session.get('google_token')

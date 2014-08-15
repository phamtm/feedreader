from flask import g
from flask.ext.httpauth import HTTPBasicAuth

from app.models import User, AnonymousUser


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    """ Verify user via HTTP Authentication. """
    if email == '':
        g.current_user = AnonymousUser()
        return True

    user = User.query.filter_by(email=email).first()

    if not user:
        return False

    g.current_user = user

    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

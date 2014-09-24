"""
On a production server, the login route must be made available over secure
HTTP so that the form data transmitted to the server is encrypted. Without
the secure HTTP, the login credentials can be intercepted during transit,
defeating any efforts put into securing passwords in the server.
"""

from flask import (redirect,
                   render_template,
                   flash,
                   request,
                   url_for,
                   session,
                   request)

from flask.ext.login import (login_required,
                             login_user,
                             logout_user,
                             current_user)

from app.decorators import unauthenticated_required
from app.forms import LoginForm
from app.mod_auth import mod_auth
from app.models import FeedSource, FeedSubscription, User


@mod_auth.route('/login', methods=['GET', 'POST'])
@unauthenticated_required
def login():
    """Logging in the user."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Do not allow user who registered with a social account to log
        # via the login form. Use the social login buttons instead
        if user is not None and user.register_with_provider:
            flash('Please login with your social account')
            return redirect(url_for('mod_auth.login'))

        if user is not None and user.verify_password(form.password.data):
            # The user must be activated
            if not user.confirmed:
                flash('You need to activate your account first')
                return redirect(url_for('mod_auth.login'))

            # Log the user in
            login_user(user, remember=form.remember.data)
            return redirect(request.referrer or url_for('mod_feed.index'))

        # Redirect to login page with an error message
        flash('Invalid email, password')

    return render_template('auth/login.html', form=form)


@mod_auth.route('/logout')
def logout():
    """Logging the user out."""

    if current_user.is_authenticated():
        logout_user()
        session['subscriptions'] = None
        flash('You have been logged out')
    return redirect(url_for('mod_feed.index'))

from flask import (redirect,
                   render_template,
                   flash,
                   url_for,
                   current_app)
from flask.ext.login import current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db
from app.mod_auth import mod_auth
from app.forms import RegisterForm
from app.models import User
from app.email import send_email
from app.decorators import unauthenticated_required



@mod_auth.route('/register', methods=['GET', 'POST'])
@unauthenticated_required
def register():
    """Register the user directly (not through a social account)."""

    if current_user.is_authenticated():
        return redirect(url_for('mod_feed.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        # Register User into database
        user = User(email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # Send email to confirm user
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your Account',
                   'auth/email/confirm', user=user, token=token)

        flash('An activation email has been sent to your account')
        return redirect(url_for('mod_feed.index'))

    return render_template('auth/register.html', form=form)


@mod_auth.route('/activate/<token>')
def activate(token):
    """Activate the registered account. The user can used the application
    only after activation.
    """

    serializer = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = serializer.loads(token)
    except:
        flash('Invalid or expired token')
        return redirect(url_for('mod_feed.index'))

    user = User.query.get(data['confirm_id'])
    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    flash('Your account is activated')

    return redirect(url_for('mod_auth.login'))

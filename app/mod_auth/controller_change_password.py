from flask import (render_template,
                   flash,
                   redirect,
                   url_for)

from flask.ext.login import (current_user,
                             login_required)

from app.mod_auth import mod_auth
from app.forms import ChangePasswordForm


@mod_auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Allow the user who did not register with a social account to change
    his password.
    """

    if current_user.register_with_provider:
        flash('Registered with a social account, no password is required')
        return redirect(url_for('mod_feed.index'))

    form = ChangePasswordForm()

    if form.validate_on_submit():
        flash('Password changed successfully')
        current_user.password = form.new_password.data

    return render_template('auth/change_password.html', form=form)

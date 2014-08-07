# Import flask dependencies
from flask import render_template, 	\
				  session, 			\
				  flash, 			\
				  redirect,			\
				  url_for,			\
				  request, 			\
				  current_app, 		\
				  abort

from flask.ext.login import current_user, 	\
							login_required

# Import the authentication module
from app.mod_auth import mod_auth
from app.forms import ChangePasswordForm


# Change password route
@mod_auth.route('/change_password', methods = ['GET', 'POST'])
@login_required
def change_password():
	# Only allow user who does not register with a social account
	# to change his password
	if current_user.register_with_provider:
		flash('Registered with a social account, no password is required')
		return redirect(url_for('mod_feed.index'))

	form = ChangePasswordForm()

	if form.validate_on_submit():
		flash('Password changed successfully')
		current_user.password = form.new_password.data

	return render_template('auth/change_password.html', form = form)


from flask import redirect, 					\
				  render_template, 				\
				  flash, 						\
				  request, 						\
				  url_for,						\
				  session,						\
				  request

from flask.ext.login import login_required, 	\
							login_user, 		\
							logout_user, 		\
							current_user		\

# from app import facebook
from app.models import User
from app.mod_auth import mod_auth
from app.forms import LoginForm
from app.decorators import unauthenticated_required


###############################################################################
# On a production server, the login route must be made available over secure
# HTTP so that the form data transmitted to the server is encrypted. Without
# the secure HTTP, the login credentials can be intercepted during transit,
# defeating any efforts put into securing passwords in the server.
###############################################################################

# Log in route
@mod_auth.route('/login', methods = ['GET', 'POST'])
@unauthenticated_required
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()

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

			# Log the user in, optionally set a cookie to later recover this session
			login_user(user, remember = form.remember.data)
			return redirect(request.referrer or url_for('mod_main.index'))

		# Redirect to login page with an error message
		flash('Invalid email, password')

	return render_template('auth/login.html', form = form)


# Log out route
@mod_auth.route('/logout')
def logout():
	if current_user.is_authenticated():
		logout_user()
		flash('You have been logged out')
	return redirect(url_for('mod_main.index'))


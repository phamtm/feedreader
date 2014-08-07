from flask import redirect, 		\
				  render_template, 	\
				  url_for, 			\
				  flash,			\
				  current_app
from flask.ext.login import current_user

from app import db
from app.forms import ResetPasswordRequestForm, \
					  ResetPasswordForm
from app.models import User
from app.email import send_email
from app.mod_auth import mod_auth
from app.decorators import unauthenticated_required

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Request reset password route
@mod_auth.route('/forgot', methods = ['GET', 'POST'])
@unauthenticated_required
def forgot():
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()

		if user is not None and not user.register_with_provider:
			token = user.generate_reset_token()
			send_email(user.email, 'Confirm your password request',
						'auth/email/reset', user = user, token = token)
			flash('You can now reset your password')
			flash('An email has been sent to your email address')
			return redirect(url_for('mod_feed.index'))
		else:
			flash('incorrect email / no password for social login')

	return render_template('auth/reset_password_request.html', form = form)


# Reset password route
@mod_auth.route('/reset/<token>', methods = ['GET', 'POST'])
@unauthenticated_required
def reset_password(token):
	s = Serializer(current_app.config['SECRET_KEY'])

	try:
		data = s.loads(token)
	except:
		flash('Invalid or expired token')
		return redirect(url_for('mod_feed.index'))

	form = ResetPasswordForm()

	if form.validate_on_submit():
		user = User.query.get(data['reset_id'])
		user.password = form.new_password.data
		db.session.add(user)
		db.session.commit()
		flash('Your password has been successfully changed')
		return redirect(url_for('mod_feed.index'))

	return render_template('auth/reset_password.html', form = form)


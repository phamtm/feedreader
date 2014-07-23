from flask import redirect, 		\
				  render_template, 	\
				  flash,			\
				  url_for, 			\
				  current_app
from flask.ext.login import current_user

from app import db
from app.mod_main import mod_main
from app.mod_auth import mod_auth
from app.forms import RegisterForm
from app.models import User
from app.email import send_email
from app.decorators import unauthenticated_required

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Register route
@mod_auth.route('/register', methods = ['GET', 'POST'])
@unauthenticated_required
def register():
	if current_user.is_authenticated():
		return redirect(url_for('mod_main.index'))

	form = RegisterForm()

	if form.validate_on_submit():
		# Register User into database
		user = User(email = form.email.data,
					password = form.password.data)
		db.session.add(user)
		db.session.commit()

		# Send email to confirm user
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm your Account',
				   'auth/email/confirm', user = user, token = token)

		flash('An activation email has been sent to your account')
		return redirect(url_for('mod_main.index'))

	return render_template('auth/register.html', form = form)


# Account activation route
@mod_auth.route('/activate/<token>')
def activate(token):
	s = Serializer(current_app.config['SECRET_KEY'])

	try:
		data = s.loads(token)
	except:
		flash('Invalid or expired token')
		return redirect(url_for('mod_main.index'))

	user = User.query.get(data['confirm_id'])
	user.confirmed = True
	db.session.add(user)
	db.session.commit()
	flash('Your account is activated')

	return redirect(url_for('mod_auth.login'))

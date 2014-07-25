from flask import url_for, 					\
				  request, 					\
				  session, 					\
				  flash,					\
				  redirect,					\
				  render_template
from flask.ext.login import login_user, 	\
							current_user

from app import db,							\
				facebook
from app.mod_auth import mod_auth
from app.decorators import unauthenticated_required
from app.models import User, 				\
					   Connection

from app.mod_auth.providers import provider_id


@mod_auth.route('/login/facebook')
@unauthenticated_required
def facebook_login():
	return facebook.authorize(callback =
			url_for('mod_auth.facebook_authorized',
					next = request.args.get('next') or request.referrer or url_for('mod_main.index'),
					_external = True
				)
		)


@mod_auth.route('/authorized/facebook')
@facebook.authorized_handler
def facebook_authorized(response):
	next_url = request.args.get('next') or request.referrer or url_for('mod_main.index')

	if response is None:
		flash('You denied the request to sign in')
		return redirect(next_url)

	# Store the token so we can access it later from tokengetter
	session['facebook_access_token'] = (response['access_token'], '')

	me = facebook.get('/me')
	email = me.data['email']

	# If the user is not registered, add him
	user = User.query.filter_by(email = email).first()
	if user is None:
		user = User(email = email, register_with_provider = True)
		db.session.add(user)
		db.session.commit()

	# In any case we update the authentication token in the db
	# If the user has revoked access we will have new token here
	connection = Connection.query.filter_by(
		user_id = user.id,
		provider_id = provider_id['FACEBOOK']).first()

	if connection is None:
		connection = Connection(
				user_id = user.id,
				provider_id = provider_id['FACEBOOK'],
				provider_user_id = me.data['id'],
				display_name = me.data['name'],
				image_url = 'https://graph.facebook.com/%s/picture?type=large' % (me.data['id']),
				user = user
			)
		db.session.add(connection)

	connection.oauth_token = response['access_token']

	login_user(user)

	return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
	return session.get('facebook_access_token')


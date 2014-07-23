from flask import url_for,			\
				  redirect,			\
				  url_for,			\
				  request,			\
				  flash,			\
				  session,			\
				  json
from flask.ext.login import login_user

from app import google,				\
				db
from app.mod_auth.providers import provider_id
from app.mod_auth import mod_auth
from app.decorators import unauthenticated_required
from app.models import User, 		\
					   Connection

from urllib2 import Request, urlopen, URLError


@mod_auth.route('/login/google')
@unauthenticated_required
def google_login():
	session['google_auth_next_url'] = request.referrer or			\
									  url_for('mod_main.index')	or	\
									  request.args.get('next')


	callback = url_for('mod_auth.google_authorized', _external = True)
	return google.authorize(callback = callback)


@mod_auth.route('/authorized/google')
@google.authorized_handler
def google_authorized(response):
	access_token = response['access_token']
	session['google_token'] = (access_token, '')

	headers = {'Authorization': 'OAuth '+ access_token}
	req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
				  None, headers)

	import time
	t1 = time.time()
	try:
		res = urlopen(req)
	except URLError, e:
		if e.code == 401:
			# Unauthorized - bad token
			session.pop('google_token', None)
			flash('You denied the request to sign in')
			return redirect(url_for('mod_auth.login'))

		flash('Something bad happened when signing with Google')
		return redirect(url_for('mod_auth.login'))
	t2 = time.time()

	user_info = json.loads(res.read())


	user = User.query.filter_by(email = user_info['email']).first()
	if user is None:
		user = User(email = user_info['email'], register_with_provider = True)
		db.session.add(user)
		db.session.commit()

	connection = Connection.query.filter_by(
			user_id = user.id,
			provider_id = provider_id['GOOGLE']
		).first()
	if connection is None:
		connection = Connection(
				user_id = user.id,
				provider_id = provider_id['GOOGLE'],
				provider_user_id = user_info['id'],
				display_name = user_info['name'],
				image_url = user_info['picture'],
				user = user
			)

	connection.oauth_token = access_token
	db.session.add(connection)

	login_user(user)

	flash('Login with google id = %s, email = %s, request time = %f' %
		(user_info['id'], user_info['email'], t2 - t1))

	return redirect(session.get('google_auth_next_url'))


@google.tokengetter
def get_google_oauth_token():
	return session.get('google_token')

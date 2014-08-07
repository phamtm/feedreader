from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask_oauth import OAuth
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
oauth = OAuth()

facebook = oauth.remote_app(
		name = 'facebook',
		base_url = 'https://graph.facebook.com',
		request_token_url = None,
		access_token_url = '/oauth/access_token',
		authorize_url = 'https://facebook.com/dialog/oauth',
		consumer_key = '273840802804076',
		consumer_secret = '41480f4a41cdcb5d08d2c10d68795421',
		request_token_params = {'scope': 'public_profile, email'}
	)

twitter = oauth.remote_app(
		name = 'twitter',
		# unless absolute urls are used to make requests, this will be added
		# before all URLs.  This is also true for request_token_url and others.
		base_url = 'https://api.twitter.com/1.1/',
		# where flask should look for new request tokens
		request_token_url = 'https://api.twitter.com/oauth/request_token',
		# where flask should exchange the token with the remote application
		access_token_url = 'https://api.twitter.com/oauth/access_token',
		# twitter knows two authorizatiom URLs.  /authorize and /authenticate.
		# they mostly work the same, but for sign on /authenticate is
		# expected because this will give the user a slightly different
		# user interface on the twitter side.
		authorize_url = 'https://api.twitter.com/oauth/authorize',
		# the consumer keys from the twitter application registry.
		consumer_key = 'xBeXxg9lyElUgwZT6AZ0A',
		consumer_secret = 'aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk'
	)

google = oauth.remote_app(
		name = 'google',
		base_url = 'https://www.google.com/accounts/',
		authorize_url = 'https://accounts.google.com/o/oauth2/auth',
		request_token_url = None,
		request_token_params = {
			'scope': 'https://www.googleapis.com/auth/userinfo.email',
			'response_type': 'code'
		},
		access_token_url = 'https://accounts.google.com/o/oauth2/token',
		access_token_method = 'POST',
		access_token_params={'grant_type': 'authorization_code'},
		consumer_key = '734224746159-tdqotge1i3hqu1t7aifi62p8komv2l2i.apps.googleusercontent.com',
		consumer_secret = '697NMzcRFJsBQPRqdRZOXS9W'
	)

# Endpoint for login page
login_manager.login_view = 'mod_auth.login'


def create_app(config_name = 'default'):

	# The WSGI application
	app = Flask(__name__)

	# Import the configuration from config object
	app.config.from_object(config[config_name])

	# Initialize extensions
	db.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	# Register blueprint
	from mod_main import mod_main
	from mod_auth import mod_auth
	from mod_feed import mod_feed
	from api_1_0 import api as api_1_0_blueprint
	app.register_blueprint(mod_main)
	app.register_blueprint(mod_auth)
	app.register_blueprint(mod_feed)
	app.register_blueprint(api_1_0_blueprint, url_prefix = '/api/v1.0')

	if config_name != 'production':
		from mod_mock import mod_mock
		app.register_blueprint(mod_mock)

	return app

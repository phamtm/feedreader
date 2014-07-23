import unittest
import time

from flask import url_for

from app import create_app, db
from app.models import User
from app.forms import RegisterForm

# IntegrityError from database
from sqlalchemy.exc import IntegrityError

from wtforms.validators import ValidationError


class ModAuthTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('test')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client(use_cookies = True)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()


	###########################################################################
	# Test registration #
	###########################################################################
	def test_invalid_email_registration(self):
		pass

	def test_email_existed_registration(self):
		pass

	def test_invalid_password_registration(self):
		pass

	def test_not_match_password_registration(self):
		pass

	def test_logged_in_registration(self):
		pass

	def test_register_and_login(self):
		# register a new account
		resp = self.client.post(url_for('mod_auth.register'),
			data = {
				'email': 'cat@foo.bar',
				'password': '12345678',
				'password2': '12345678'
			}
		)

		# 302 is a redirect
		self.assertTrue(resp.status_code == 302, 'Not redirect')

		# login with new account
		resp = self.client.post(url_for('mod_auth.login'),
			data = {
				'email': 'cat@foo.bar',
				'password': '12345678',
			},
			follow_redirects = True
		)
		data = resp.get_data(as_text = True)
		self.assertTrue('You need to activate your account first' in data)

		# send a confirmation token
		user = User.query.filter_by(email = 'cat@foo.bar').first()
		token = user.generate_confirmation_token()
		resp = self.client.get(url_for('mod_auth.activate', token = token),
								follow_redirects = True)
		data = resp.get_data(as_text = True)
		self.assertTrue('Your account is activated' in data)

		# logout
		resp = self.client.post(url_for('mod_auth.login'),
			data = {
				'email': 'cat@foo.bar',
				'password': '12345678',
			},
		)

		resp = self.client.get(url_for('mod_auth.logout'),
							   follow_redirects = True)
		data = resp.get_data(as_text = True)
		self.assertIn('You have been logged out', data)



	###########################################################################
	# Test activation #
	###########################################################################
	def test_invalid_token_activation(self):
		pass

	def test_logged_in_activation(self):
		pass

	def test_valid_token_activation(self):
		pass

	def test_expired_token_activation(self):
		pass


	###########################################################################
	# Test login #
	###########################################################################
	def test_already_logged_in(self):
		pass

	def test_remember_login(self):
		pass

	def test_invalid_email_login(self):
		pass

	def test_wrong_email_password_login(self):
		pass

	def test_correct_login(self):
		pass


	###########################################################################
	# Test logout #
	###########################################################################
	def test_already_logged_out(self):
		pass

	def test_correct_logout(self):
		pass


	###########################################################################
	# Test change password #
	###########################################################################



	###########################################################################
	# Test password reset #
	###########################################################################


import unittest

from flask import url_for

from app import create_app, db
from app.models import User, Connection


class TestSocialLogin(unittest.TestCase):

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


	def test_social_login_cannot_login_via_login_form(self):
		u = User(email = 'cat@house.com', register_with_provider = True)
		db.session.add(u)
		db.session.commit()

		# login with this account
		response = self.client.post(
				url_for('mod_auth.login'),
				data = {
					'email': u.email,
					'password': u.password_hash
				},
				follow_redirects = True
			)

		data = response.get_data(as_text = True)

		self.assertIn('Please login with your social account', data)


import unittest
import time

from sqlalchemy.exc import IntegrityError

from app import create_app, login_manager
from app.models import User, Permission, Role
from database import db_session, init_db, drop_db

class UserModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('test')
		self.app_context = self.app.app_context()
		self.app_context.push()
		init_db()
		Role.insert_roles()


	def tearDown(self):
		db_session.remove()
		drop_db()
		self.app_context.pop()


	def test_password_setter(self):
		u = User(password = 'cat')
		self.assertTrue(u.password_hash is not None)


	def test_no_password_getter(self):
		u = User(password = 'cat')
		with self.assertRaises(AttributeError):
			u.password


	def test_password_verification(self):
		u = User(password = 'cat')
		self.assertTrue(u.verify_password('cat'))
		self.assertFalse(u.verify_password('dog'))


	def test_password_salts_are_random(self):
		u1 = User(password = 'cat')
		u2 = User(password = 'cat')
		self.assertTrue(u1.password_hash != u2.password_hash)


	def test_require_email(self):
		u = User(password = 'cat')
		db_session.add(u)
		with self.assertRaises(IntegrityError):
			db_session.commit()


	def test_valid_confirmation_token(self):
		u = User(email = 'cat@house.com', password = 'cat')
		db_session.add(u)
		db_session.commit()
		token = u.generate_confirmation_token()
		self.assertTrue(u.confirm(token))


	def test_invalid_confirmation_token(self):
		u1 = User(email = 'cat@house.com', password = 'cat')
		u2 = User(email = 'dog@house.com', password = 'dog')
		db_session.add(u1)
		db_session.add(u2)
		db_session.commit()
		token = u1.generate_confirmation_token()
		self.assertFalse(u2.confirm(token))


	def test_expired_confirmation_token(self):
		u = User(email = 'cat@house.com', password = 'cat')
		db_session.add(u)
		db_session.commit()
		token = u.generate_confirmation_token(1)
		time.sleep(2)
		self.assertFalse(u.confirm(token))


	def test_default_user_permission(self):
		u = User(email = 'cat@house.com', password = 'cat')
		db_session.add(u)
		db_session.commit()
		self.assertTrue(u.has_permissions(Permission.FOLLOW))
		self.assertFalse(u.has_permissions(Permission.MODERATE_COMMENTS))


	def test_admin_user_permission(self):
		u = User(email = self.app.config['ADMIN_EMAIL'], password = 'cat')
		db_session.add(u)
		db_session.commit()
		self.assertTrue(u.has_permissions(Permission.FOLLOW))


	def test_anonymous_user_permission(self):
		u = login_manager.anonymous_user()
		self.assertFalse(u.has_permissions(Permission.FOLLOW))

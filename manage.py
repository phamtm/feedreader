import os
from app import create_app, db
from app.models import Connection, FeedArticle, FeedProvider, FeedSource, FeedSubscription, User, Role, Permission
from app.mod_feed.sources import feed_sources
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def createdb():
	db.drop_all()
	db.create_all()
	Role.insert_roles()

	# Insert feedprovider
	for site in feed_sources:
		provider_name = site['name']
		provider_domain = site['domain']
		provider = FeedProvider(name = provider_name, domain = provider_domain)
		db.session.add(provider)
		db.session.commit()

		# Add feedsource
		for channel_name in site['channels']:
			source_name = site['name'] + ' - ' + channel_name
			source_href = site['channels'][channel_name]
			fs = FeedSource(name = source_name, href = source_href, provider = provider)
			db.session.add(fs)

	db.session.commit()


@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def listusers():
	User.query.all()

@manager.command
def listconnections():
	Connection.query.all()


if __name__ == '__main__':
	manager.run()

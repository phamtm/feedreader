import os
import time

from flask.ext.script import Manager, Shell
import yaml

from app import celery, create_app, db
from app.models import (Connection,
						FeedArticle,
						FeedProvider,
						FeedSource,
						FeedSubscription,
						Magazine,
						MagazineArticle,
						FollowUser,
						Friendship,
						Permission,
						User,
						Role)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
db.init_app(app)
manager = Manager(app)


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def createdb():
	print 'creating db..'
	db.drop_all()
	db.create_all()
	Role.insert_roles()

	print 'adding feed sources..'
	with open('sources.yaml', 'r') as f:
		feed_sources = yaml.load(f)

	# Insert feedprovider
	for site in feed_sources:
		provider_name = unicode(site['name'])
		provider_domain = site['domain']
		provider = FeedProvider(name = provider_name,
								domain = provider_domain,
								favicon = site['favicon'])
		db.session.add(provider)
		db.session.commit()

		# Add feedsource
		for channel_name in site['channels']:
			source_name = unicode(site['name'] + ' - ' + channel_name)
			source_href = site['channels'][channel_name]
			fs = FeedSource(name=source_name, url=source_href, provider=provider)
			db.session.add(fs)

	db.session.commit()

	print 'add feed articles..'
	from app.mod_crawler.fetch import update_db
	update_db()

	# tfidf()


@manager.command
def tfidf():
	print 'computing relevant articles..'
	t0 = time.time()
	from app.recommender.related_articles import compute_simmilarity
	compute_similarity()
	t1 = time.time()
	print '-- Elapsed time: %.3f' % (t1 - t0)
	# db.session.commit()



@manager.command
def updatedb():
	from app.mod_crawler.fetch import update_db
	update_db()


@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def dumpdb():
	articles = FeedArticle.query.filter_by(source_id = 2).all()
	titles = [a.title.encode('utf-8') for a in articles]
	for idx, title in enumerate(titles):
		with open('data/%d.txt' % (idx), 'w') as f:
			f.write(title)

@manager.command
def run():
    app.run(debug=True)


if __name__ == '__main__':
	manager.run()

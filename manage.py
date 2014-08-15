import os
import time

from flask.ext.script import Manager, Shell

from app import celery, create_app, db
from app.models import (Connection,
						FeedArticle,
						FeedProvider,
						FeedSource,
						FeedSubscription,
						User,
						Role,
						Permission)
from app.mod_crawler.sources import feed_sources

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
	# Insert feedprovider
	for site in feed_sources:
		provider_name = unicode(site['name'])
		provider_domain = site['domain']
		provider = FeedProvider(name = provider_name, domain = provider_domain)
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
def testcommit():
	import forgery_py
	num_articles = 4
	articles = []
	from random import shuffle
	from app.mod_crawler.fetch import addarticle
	s = 'qwertyuiopasdfghjklzxcvbnm'
	for i in range(num_articles):
		article = FeedArticle(
			title=forgery_py.lorem_ipsum.sentence(),
			link=forgery_py.internet.domain_name() + '/' + s,
			summary=forgery_py.lorem_ipsum.paragraph(),
			html_readable=forgery_py.lorem_ipsum.paragraph(),
			source_id=1,
			thumbnail_url=forgery_py.internet.domain_name() + '/' + s + '.jpg'
		)
		articles.append(article)

	for a in articles:
		addarticle.delay(a, db)



@manager.command
def tfidf():
	print 'computing relevant articles..'
	t0 = time.time()
	from app.recommender.related_article import compute_tfidf
	compute_tfidf()
	t1 = time.time()
	print '-- Elapsed time: %.3f' % (t1 - t0)
	# db.session.commit()



@manager.command
def updatefeed():
	from app.mod_feed import fa
	fa.update_db()


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

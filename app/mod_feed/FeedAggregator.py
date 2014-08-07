from app import db
from app.utils import Future
from app.models import FeedArticle,		\
					   FeedProvider,	\
					   FeedSource

from app.mod_crawler.thumbnail import get_thumbnail_src
from app.mod_crawler.article import fetch_readable,				\
									fetch_thumbnail_from_html

from breadability.readable import Article
import urllib2
import feedparser


class FeedAggregator(object):

	def update_db(self):
		entries = self.get_all_feeds()
		self.add_feed_entries_to_db(entries)


	def get_all_feeds(self):
		sources = [(source.id, source.href) for source in FeedSource.query.all()]

		entries = []
		for source in sources:
			source_id = source[0]
			source_url = source[1]
			print 'Fetching rss from <%s>' % source_url
			source_entries = self.get_feed_entries_from_source(source_url)
			if source_entries:
				entries.append((source_id, source_entries))

		return entries


	def get_feed_entries_from_source(self, url):
		feeds = feedparser.parse(url)

		# Return None if feeds is not well formed or not found
		if feeds.bozo or feeds.status != 200:
			return None

		return feeds.entries


	# Create a FeedArticle object from a raw (dictionary) entry.
	# Return None if not a valid entry
	def get_feed_article(self, source_id, entry):
		article = None

		if 'title' in entry and 'link' in entry:
			article = FeedArticle(
				title = unicode(entry.title),
				link = unicode(entry.link),
				source_id = source_id)

			# Summary is optional
			if 'summary' in entry:
				article.summary = unicode(entry.summary)

			readable = fetch_readable(article.link)
			article.readable_content = readable
			article.thumbnail_url = fetch_thumbnail_from_html(readable, article.summary)

		return article


	# Create a FeedArticle from the entry and add to database
	def add_feed_entry_to_db(self, source_id, entry):
		article = self.get_feed_article(source_id, entry)

		old_article = FeedArticle.query.filter_by(
				source_id = article.source_id,
				link = article.link
			).first()

		if article and not old_article:
			db.session.add(article)
			db.session.commit()


	# Create a FeedArticle from each entry and add to database
	def add_feed_entries_to_db(self, entries):
		for entry in entries:
			source_id, source_entries = entry
			for idx, source_entry in enumerate(source_entries):
				print '%3d/%d %s' % (idx, len(source_entries), source_entry.link)
				self.add_feed_entry_to_db(source_id, source_entry)


	def __repr__(self):
		return '<FeedAggregator>'

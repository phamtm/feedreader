from app import db
from app.utils import Future
from app.models import FeedArticle,		\
					   FeedProvider,	\
					   FeedSource

import feedparser

# future_calls = [(source.id, Future(feedparser.parse, source['href'])) for source in sources]
# feeds = [(future_obj[0], future_obj[1]()) for future_obj in future_calls]


class FeedAggregator(object):

	def update_feed_db(self):
		entries = self.get_all_feeds()
		self.add_feed_entries_to_db(entries)


	def get_all_feeds(self):
		sources = [(source.id, source.href) for source in FeedSource.query.all()]

		entries = []
		for source in sources:
			source_id = source[0]
			source_href = source[1]
			source_entries = self.get_feed_entries_from_source(source_href)
			if source_entries is not None:
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
		if 'title' in entry and 'link' in entry:
			article = FeedArticle(
				title = unicode(entry.title),
				link = unicode(entry.link),
				source_id = source_id)

			# Summary is optional
			if 'summary' in entry:
				article.summary = unicode(entry.summary)

			return article

		return None


	# Create a FeedArticle from the entry and add to database
	def add_feed_entry_to_db(self, source_id, entry):
		article = self.get_feed_article(source_id, entry)

		old_article = FeedArticle.query.filter_by(
				source_id = article.source_id,
				link = article.link
			).first()

		if article is not None and old_article is None:
			db.session.add(article)
			db.session.commit()


	# Create a FeedArticle from each entry and add to database
	def add_feed_entries_to_db(self, entries):
		for entry in entries:
			source_id, source_entries = entry
			for source_entry in source_entries:
				self.add_feed_entry_to_db(source_id, source_entry)



	def __repr__(self):
		return '<FeedAggregator>'


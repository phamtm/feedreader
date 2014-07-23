from app.models import FeedArticle,		\
					   FeedProvider,	\
					   FeedSource
import feedparser
from app.utils import Future



class FeedAggregator(object):

	def get_all_feeds(self):
		# sources = [{
		# 		'id': source.id,
		# 		'href': source.href
		# 	} for source in FeedSource.query.all()]

		# # Send out multiple request at once
		# future_calls = [(source.id, Future(feedparser.parse, source['href'])) for source in sources]
		# feeds = [(future_obj[0], future_obj[1]() for future_obj in future_calls]

		# # Extract all entries
		# entries = []
		# for feed in feeds:
		# 	entries += fee
		# print len(entries)
		# print entries[0].keys()

		# articles = [FeedArticle(
		# 	title = e.title,
		# 	link = e.link,
		# 	provider_article_id = e.id) for e in entries]
		pass


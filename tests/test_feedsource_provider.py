import unittest

from app.models import FeedSource


class TestFeedProviderModel(unittest.TestCase):

	def test_invalid_domain(self):
		invalid_urls = [
				# empty string
				''

				# no http://
				'foo.bar',

				# no suffix
				'http://foo',
				'http://foo:12345',

				# non alpha numeric or '-'
				'http://@.foo.bar/',
				'http://www.foo@.bar',
				'http://www.foo.bar@',
				'http://www.foo.bar:abc',
				'http://www.foo.bar:@',

				# invalid port
				'http://foo.bar:abc'

				# invalid extension
				'http://foo.bar:abc/rss'
				'http://foo.bar:abc/.rss'
				'http://foo.bar:abc/a.rss'
			]



	def test_valid_domain(self):
		valid_urls = [
				'http://foo.bar/a.rss',
				'http://foo.bar/123.rss',
				'http://www.foo.bar/a/b.rss'
				'http://foo.bar:5000/a/1.rss',
				'http://www.foo.bar:5000/1/2.rss'
			]

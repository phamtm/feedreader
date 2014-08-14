import unittest

from app.models import FeedProvider

class TestFeedProviderModel(unittest.TestCase):
	def test_invalid_source_url(self):
		invalid_urls = [
				# empty string
				''

				# no http://
				'foo.bar'

				# no suffix
				'http://foo'
				'http://foo:12345'

				# non alpha numeric or '-'
				'http://@.foo.bar/'
				'http://www.foo@.bar'
				'http://www.foo.bar@'
				'http://www.foo.bar:abc'
				'http://www.foo.bar:@'

				# invalid port
				'http://foo.bar:abc'
			]

		for url in invalid_urls:
			self.assertTrue(not FeedProvider.domain_regex.match(url))


	def test_valid_source_url(self):
		valid_urls = [
				'http://foo.bar',
				'http://foo.bar/',
				'http://www.foo.bar'
				'http://foo.bar:5000/',
				'http://www.foo.bar:5000',
				'http://www.foo.bar:5000/',
			]

		for url in valid_urls:
			self.assertTrue(FeedProvider.domain_regex.match(url))

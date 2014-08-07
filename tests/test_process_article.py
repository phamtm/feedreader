import unittest
from app.mod_crawler.article import fetch_readable,		\
									fetch_thumbnail

class TestProcessArticle(unittest.TestCase):
	def test_readability(self):
		with open('tests/urls.txt') as f:
			for line in f:
				self.assertTrue(fetch_readable(line))

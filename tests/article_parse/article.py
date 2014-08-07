from breadability.readable import Article
from urllib2 import urlopen, HTTPError, URLError
from BeautifulSoup import BeautifulSoup

# Get readable html content
def fetch_readable(url):
	readable = None

	try:
		file_object = urlopen(url)

	except (ValueError, URLError, HTTPError) as e:
		print 'ERROR: %s' % url
		if e:
			print e
		return None

	else:
		html = file_object.read()

		# Parse readable html
		article = Article(html, url)
		readable = article.readable

	finally:
		return readable
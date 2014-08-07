from app.models import FeedArticle
from app.mod_crawler.thumbnail import get_thumbnail_src
from breadability.readable import Article
from urllib2 import urlopen, HTTPError, URLError
from BeautifulSoup import BeautifulSoup

# Get readable html content
def fetch_readable(url):
	readable = None

	try:
		file_object = urlopen(url)

	except (ValueError, URLError, HTTPError) as e:
		print url
		print e
		return None

	else:
		html = file_object.read()

		# Parse readable html
		article = Article(html, url)
		readable = article.readable

	finally:
		return readable


# Get article's thumbnail
def fetch_thumbnail(url, summary = None):
	if summary:
		thumbnail_url = get_thumbnail_src(summary)
		if thumbnail_url:
			return thumbnail_url

	html = fetch_readable(url)
	return get_thumbnail_src(html)


# Get article's thumbnail from html
def fetch_thumbnail_from_html(readable_content, summary = None):
	if summary:
		thumbnail_url = get_thumbnail_src(summary)
		if thumbnail_url:
			return thumbnail_url

	return get_thumbnail_src(readable_content)
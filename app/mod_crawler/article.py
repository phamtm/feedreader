from app.models import FeedArticle
from app.mod_crawler.thumbnail import get_thumbnail_src
from breadability.readable import Article
from urllib2 import urlopen, HTTPError, URLError
from app import celery


@celery.task
def fetch_html(url):
    html = None

    try:
        file_object = urlopen(url)
    except (ValueError, URLError, HTTPError) as e:
        print e, url
        return None

    html = file_object.read()
    return html


@celery.task
def get_readable(html, url):
    # Parse readable html
    article = Article(html, url)
    readable = article.readable
    return readable


# Get article's thumbnail
def get_thumbnail_from_summary(summary):
    if summary:
        thumbnail_url = get_thumbnail_src(summary)
        if thumbnail_url:
            return thumbnail_url
    return None


def fetch_thumbnail_from_url(url):
    html = fetch_readable(url)
    return get_thumbnail_src(html)


# Get article's thumbnail from html
def fetch_thumbnail_from_html(readable_content, summary = None):
    if summary:
        thumbnail_url = get_thumbnail_src(summary)
        if thumbnail_url:
            return thumbnail_url

    return get_thumbnail_src(readable_content)
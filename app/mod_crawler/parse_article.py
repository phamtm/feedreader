from urllib2 import urlopen, HTTPError, URLError

from breadability.readable import Article

from app import celery
from app.models import FeedArticle


@celery.task
def fetch_html(url):
    html = None

    try:
        file_object = urlopen(url)
    except (ValueError, URLError, HTTPError) as e:
        print e, url
        return None

    try:
        html = file_object.read()
    except Exception:
        return None

    return html


@celery.task
def get_readable(html, url):

    if not html:
        return None

    # Parse readable html
    try:
        article = Article(html, url)
    except:
        print 'Readable error: <%s>' % url
        return None
    return article.readable

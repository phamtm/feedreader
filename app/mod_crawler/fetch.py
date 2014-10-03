import time
import urllib
from urllib2 import urlopen, HTTPError, URLError

from breadability.readable import Article
from bs4 import BeautifulSoup
import feedparser
from flask import current_app

from app import celery, db, cdb
from app.mod_crawler.parse_article import fetch_html, get_readable
from app.mod_crawler.parse_thumbnail import get_thumbnail_url_from_summary
from app.models import FeedArticle, FeedProvider, FeedSource


@celery.task(ignore_result=True)
def add_article(source_id, entry):
    if FeedArticle.query.filter_by(link=entry.link, source_id=source_id).first():
        return

    summary = BeautifulSoup(entry.summary, 'lxml').get_text()
    article = FeedArticle(
        link=entry.link,
        title=entry.title,
        summary=summary,
        source_id=source_id,
        html=entry.summary)

    if 'media_thumbnail' in entry:
        article.thumbnail_url = entry['media_thumbnail'][0]['url']

    if not article.thumbnail_url and 'links' in entry:
        links = entry['links']
        for link in links:
            if 'type' in link and link['type'].startswith('image'):
                if 'href' in link:
                    article.thumbnail_url = link['href']
                    break

    if article.summary and not article.thumbnail_url:
        article.thumbnail_url = get_thumbnail_url_from_summary(article.html)

    cdb.session.add(article)
    cdb.session.commit()


@celery.task(ignore_result=True)
def update_db():
    # 1. Fetch all entries
    sources = FeedSource.query.all()
    # 2. Fetch articles
    for source in sources:
        chain = fetch_url_data.s(source.id, source.url) | parse_feed.s()
        chain.apply_async()


@celery.task
def fetch_url_data(source_id, url):
    data = None

    try:
        file_object = urlopen(url)
    except (ValueError, URLError, HTTPError) as e:
        print e, url
        return None

    try:
        data = file_object.read()
    except Exception:
        return None

    retval = {
        'source_id': source_id,
        'data': data}

    return retval


@celery.task
def parse_feed(data):
    feeds = feedparser.parse(data['data'])

    # TODO: Deal with not well-formed xml detection (feeds.bozo == 1)

    # Return None if feeds is not well formed or not found
    # if feeds.bozo or feeds.get('status') != 200:
    #     print '\tCannot fetch from source <%s>' % url
    #     return None

    if 'entries' in feeds:
        for entry in feeds.entries:
            add_article.delay(data['source_id'], entry)


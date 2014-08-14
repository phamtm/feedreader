import time

from flask import current_app
from breadability.readable import Article
import feedparser
from bs4 import BeautifulSoup

from app import celery
from app.utils import Future
from app.models import FeedArticle, FeedProvider, FeedSource
from app.mod_crawler.thumbnail import get_thumbnail_src
from app.mod_crawler.article import (fetch_html,
                                     get_readable,
                                     get_thumbnail_from_summary)
from app.recommender.vnstemmer import vnstring_to_ascii
from database import db_session, cdb_session


@celery.task(ignore_result=True)
def add_article(readable_content, article):
    article.readable_content = readable_content
    cdb_session.add(article)
    cdb_session.commit()


def update_db():
    """
    Updatedb steps:
        1. fetch_entries
            [(src_id, entry)]
        2. fetch_article
            [
                article:
                    title
                    link
                    summary
                    summary_ascii

                    readable -> html
                    thumbnail_url
            ]
        3. add_to_db
    """

    # 1. Fetch all entries
    t0 = time.time()
    results = fetch_all_entries()
    t1 = time.time()
    print 'Fetching entries takes %.3fs' % (t1 - t0)
    print 'Num entries %d' % (len(results))

    # 2. Fetch articles
    for result in results:
        source_id, entry = result

        if not FeedArticle.query.filter_by(link=entry.link, source_id=source_id).first():
            article = FeedArticle(
                link=entry.link,
                title=entry.title,
                summary=entry.summary,
                source_id=source_id
            )

            chain = fetch_html.s(entry.link) |          \
                    get_readable.s(entry.link) |        \
                    add_article.s(article)

            chain.apply_async()


def fetch_all_entries():
    sources = FeedSource.query.all()

    asyncs = []
    for source in sources:
        print 'Fetching from source <%s>' % source.url
        async = fetch_entries_from_source.delay(source.url)
        asyncs.append((source.id, async))

    all_entries = []
    for tup in asyncs:
        source_id, async = tup
        entries = async.wait()
        if entries:
            all_entries.extend([(source_id, entry) for entry in entries])

    return all_entries


@celery.task
def fetch_entries_from_source(url):
    feeds = feedparser.parse(url)

    # TODO: Deal with not well-formed xml detection (feeds.bozo == 1)

    # Return None if feeds is not well formed or not found
    if feeds.status != 200:
        print '\tCannot fetch from source <%s>' % url
        return None

    return feeds.entries

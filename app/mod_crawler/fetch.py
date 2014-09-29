import time

from breadability.readable import Article
from bs4 import BeautifulSoup
import feedparser
from flask import current_app

from app import celery, db, cdb
from app.mod_crawler.parse_article import fetch_html, get_readable
from app.mod_crawler.parse_thumbnail import get_thumbnail_url_from_summary
from app.models import FeedArticle, FeedProvider, FeedSource


@celery.task(ignore_result=True)
def add_article(article):
    if article.summary and not article.thumbnail_url:
        article.thumbnail_url = get_thumbnail_url_from_summary(article.html)

    # if not article.thumbnail_url:
    #     article.thumbnail_url = get_thumbnail_url_from_html(html_readable)

    cdb.session.add(article)
    cdb.session.commit()


@celery.task(ignore_result=True)
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
                    summary_stemmed

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
            summary = BeautifulSoup(entry.summary, 'lxml').get_text()
            article = FeedArticle(
                link=entry.link,
                title=entry.title,
                summary=summary,
                source_id=source_id,
                html=entry.summary
            )

            if 'media_thumbnail' in entry:
                article.thumbnail_url = entry['media_thumbnail'][0]['url']

            if not article.thumbnail_url and 'links' in entry:
                links = entry['links']
                for link in links:
                    if 'type' in link and link['type'].startswith('image'):
                        if 'href' in link:
                            article.thumbnail_url = link['href']
                            break

            # chain = fetch_html.s(entry.link) |          \
            #         get_readable.s(entry.link) |        \
            #         add_article.s(article)
            # chain.apply_async()

            add_article.delay(article)


def fetch_all_entries():
    sources = FeedSource.query.all()

    print 'nsources: %d' % len(sources)

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
    # if feeds.bozo or feeds.get('status') != 200:
    #     print '\tCannot fetch from source <%s>' % url
    #     return None

    return feeds.entries

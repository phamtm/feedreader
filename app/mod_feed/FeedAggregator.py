from app import db
from app.utils import Future
from app.models import FeedArticle,     \
                       FeedProvider,    \
                       FeedSource

from app.mod_crawler.thumbnail import get_thumbnail_src
from app.mod_crawler.article import fetch_readable,             \
                                    fetch_thumbnail_from_html
from app.recommender.vnstemmer import vnstring_to_ascii

from flask import current_app
from breadability.readable import Article
import urllib2
import feedparser
from bs4 import BeautifulSoup

import time

class FeedAggregator(object):

    def update_db(self):
        entries = self.get_all_feeds()
        # self.add_feed_entries_to_db(entries)


    def get_all_feeds(self):
        sources = [(src.id, src.href) for src in FeedSource.query.all()]

        entries = []
        t0 = time.time()
        for source in sources:
            source_id = source[0]
            source_url = source[1]
            print 'Fetching rss from <%s>' % source_url
            source_entries = self.get_feed_entries_from_source(source_url)
            if source_entries:
                entries.append((source_id, source_entries))
            else:
                print 'Warning: cannot fetch rss from <%s>' % (source_url)

        t1 = time.time()
        print '\tFetching RSS takes: %.3fs' % (t1 - t0)
        return entries


    # @current_app.celery.task()
    def get_feed_entries_from_source(self, url):
        feeds = feedparser.parse(url)

        # TODO: Deal with not well-formed xml detection (feeds.bozo == 1)

        # Return None if feeds is not well formed or not found
        if feeds.status != 200:
            return None

        # Testing: return 5 entries only
        return feeds.entries


    # Create a FeedArticle object from a raw (dictionary) entry.
    # Return None if not a valid entry
    def to_article(self, source_id, entry):
        article = None

        if 'title' in entry and 'link' in entry:
            article = FeedArticle(
                title=unicode(entry.title),
                link=unicode(entry.link),
                source_id=source_id)

            # Summary is optional
            if 'summary' in entry:
                soup = BeautifulSoup(entry.summary, 'lxml')
                stripped_summary = ' '.join(soup.findAll(text=True))
                article.summary = unicode(stripped_summary)
                article.summary_ascii = unicode(vnstring_to_ascii(stripped_summary))

            readable = fetch_readable(article.link)
            article.readable_content = readable
            article.thumbnail_url = fetch_thumbnail_from_html(readable, entry.summary)

        return article


    # Create a FeedArticle from the entry and add to database
    def add_feed_entry_to_db(self, source_id, entry):
        article = self.to_article(source_id, entry)

        old_article = FeedArticle.query.filter_by(
            source_id=article.source_id,
            link=article.link
        ).first()

        if article and not old_article:
            db.session.add(article)
            db.session.commit()


    # Create a FeedArticle from each entry and add to database
    def add_feed_entries_to_db(self, entries):
        t0 = time.time()
        for entry in entries:
            source_id, source_entries = entry
            print 'Adding from source %d' % (source_id)
            for idx, source_entry in enumerate(source_entries):
                print '%3d/%d %s' % (
                    idx, len(source_entries), source_entry.link)
                self.add_feed_entry_to_db(source_id, source_entry)

        t1 = time.time()
        dt = t1 - t0
        nentries = sum(len(e[1]) for e in entries)
        avg = 0
        if nentries > 0:
            avg = dt / nentries
        print 'Article processing takes: %.3fs' % (dt)
        print 'Number of article: %d' % nentries
        print 'Average time per article: %.3f' % (avg)

    def __repr__(self):
        return '<FeedAggregator>'

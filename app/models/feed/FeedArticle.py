from app import db
from app.utils import wilson_score
from ..Base import Base

from bs4 import BeautifulSoup
import urllib2

MIN_AREA = 250 * 100


class FeedArticle(db.Model):

    __tablename__       = 'feedarticle'

    __table_args__      = (
            db.UniqueConstraint('link', 'source_id'),
        )

    id                  = db.Column(db.Integer, primary_key = True)
    title               = db.Column(db.Unicode(255, convert_unicode = True), nullable = False)
    link                = db.Column(db.String(511))
    summary             = db.Column(db.UnicodeText(convert_unicode = True))
    summary_ascii       = db.Column(db.UnicodeText(convert_unicode = True))
    thumbnail_url       = db.Column(db.String(511))
    time_published      = db.Column(db.DateTime, default = db.func.current_timestamp())

    # Related articles (csv)
    related_articles    = db.Column(db.String(127), default = '')

    # Readablility processed article
    readable_content    = db.Column(db.UnicodeText(convert_unicode = True), nullable = True)

    # Vote records
    upvote              = db.Column(db.Integer, default = 0)
    downvote            = db.Column(db.Integer, default = 0)
    wilson_score        = db.Column(db.Float, default = 0.0)
    views               = db.Column(db.Integer, default = 0)

    source_id           = db.Column(db.Integer, db.ForeignKey('feedsource.id'))


    def update_wilson_score(self):
        self.wilson_score = wilson_score(self.upvote, self.upvote + self.downvote)


    def get_related_articles(self):
        return map(int, self.related_articles.split())


    def __repr__(self):
        return '<FeedArticle %s %s>' % (self.title.encode('utf-8'), self.link.encode('utf-8'))





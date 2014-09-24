from sqlalchemy import (Boolean, Column, Integer, ForeignKey, Unicode)
from sqlalchemy.orm import backref, relationship

from app import db
from app.models.user.MagazineArticle import MagazineArticle
from app.models.feed.FeedArticle import FeedArticle
from app.models.Base import Base


class Magazine(Base):
    __tablename__ = 'magazine'

    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(Unicode(255, convert_unicode=True), nullable=False)
    public = Column(Boolean, default=True)
    article_ids = relationship('MagazineArticle',
                               backref='magazine',
                               lazy='dynamic')


    def get_articles(self):
        """Return a list of article in this magazine"""
        articles = FeedArticle.query                            \
            .join(MagazineArticle,                              \
                  MagazineArticle.article_id == FeedArticle.id) \
            .filter_by(magazine_id = magazine_id)

        return articles


    def add_article(self, article_id):
        """Add an article's id to this magazine"""

        if not MagazineArticle.query.filter_by(
            magazine_id=self.id,
            article_id=article_id).first():
            magart = MagazineArticle(magazine_id=self.id,
                                     article_id=article_id)
            db.session.add(magart)
            db.session.commit()


    def remove_article(self, article_id):
        """Remove an article's id from this magazine"""

        if MagazineArticle.query.filter_by(
            magazine_id=self.id,
            article_id=article_id).first():
            magart = MagazineArticle(magazine_id=self.id,
                                     article_id=article_id)
            db.session.remove(magart)
            db.session.commit()

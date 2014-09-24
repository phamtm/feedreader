from sqlalchemy import (Column, DateTime, Integer, ForeignKey, func)

from app import db


class MagazineArticle(db.Model):
    __tablename__ = 'magazinearticle'

    id = Column(Integer, primary_key=True)
    magazine_id = Column(Integer, ForeignKey('magazine.id'))
    article_id = Column(Integer, ForeignKey('feedarticle.id'))
    date_created = Column(DateTime, default=func.current_timestamp())

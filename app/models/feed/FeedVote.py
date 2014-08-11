from app import db



class FeedVote(db.Model):

    __tablename__   = 'feedvote'

    __table_args__  = (
            db.PrimaryKeyConstraint('user_id', 'article_id'),
        )

    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id      = db.Column(db.Integer, db.ForeignKey('feedarticle.id'))
    is_upvote       = db.Column(db.Boolean, default = True)

    date_created    = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified   = db.Column(db.DateTime,
                        default = db.func.current_timestamp(),
                        onupdate = db.func.current_timestamp())


    def __repr__(self):
        return '<FeedVote article_id=%d, user_id=%s, is_upvote=%d>' \
                % (self.article_id, self.user_id, self.is_upvote)
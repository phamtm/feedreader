from flask import abort, jsonify, request, g

from app.api_1_0 import api
from app.api_1_0.authentication import auth
from app.models import FeedArticle, FeedVote, Magazine


@api.route('/article/get')
def get_article():
    article_id = request.args.get('article_id', type=int)
    if not article_id:
        abort(404)

    article = FeedArticle.query.get(article_id)
    if not article:
        abort(404)

    return jsonify({
        'title':article.title,
        'link':article.link,
        'thumbnail_url':article.thumbnail_url,
        'summary':article.summary})


@api.route('/article/add_to_magazine')
def add_to_magazine():
    article_id = request.args.get('article_id', type=int)
    magazine_id = request.args.get('magazine_id', type=int)

    if not article_id or not magazine_id or not FeedArticle.query.get(article_id):
        abort(404)

    magazine = Magazine.query.filter_by(
        user_id=g.current_user.id,
        id=magazine_id).first()

    if not magazine:
        abort(404)

    res = magazine.add_article(article_id)
    if res:
        response = jsonify({'result':'success'})
    else:
        response = jsonify({'result':'error'})

    return response


@api.route('/article/upview')
def upview():
    """Increase the views of the article."""

    article_id = request.args.get('article_id')

    if not article_id:
        abort(404)

    article = FeedArticle.query.get(article_id)

    if not article:
        abort(404)

    article.views += 1

    return jsonify({
        'article_id': article_id,
        'article_views': article.views})


@api.route('/article/upvote')
def upvote():
    """Increase the vote of the article"""

    article_id = request.args.get('article_id')

    if not article_id:
        abort(404)

    article = FeedArticle.query.get(article_id)
    if not article:
        abort(404)

    vote = FeedVote.query.get((g.current_user.id, article_id))

    # No vote from the user yet, add one
    if not vote:
        vote = FeedVote(
            user_id=current_user.id,
            article_id=article_id,
            is_upvote=True)

        article.upvote += 1
        article.update_wilson_score()
        db.session.add(vote)
    else:
        if not vote.is_upvote:
            vote.is_upvote = True
            article.upvote += 1
            article.downvote -= 1
            article.update_wilson_score()

    return jsonify({
        'article_id': article_id,
        'upvote': article.upvote})


@api.route('/article/downvote')
def downvote():
    """Decrease the vote of the article."""

    article_id = request.args.get('article_id')

    if not article_id:
        return redirect(url_for('mod_main.all_feeds'))

    article = FeedArticle.query.get(article_id)
    if not article:
        abort(404)

    vote = FeedVote.query.get((user_id, article_id))

    # No vote from the user yet, add one
    if not vote:
        vote = FeedVote(
            user_id=current_user.id,
            article_id=article_id,
            is_upvote=False)
        article.downvote += 1
        article.update_wilson_score()
        db.session.add(vote)
    else:
        if vote.is_upvote:
            vote.is_upvote = False
            article.upvote -= 1
            article.downvote += 1
            article.update_wilson_score()

    return jsonify({
        'article_id': article_id,
        'upvote': article.upvote})


@api.route('/article/remove_vote')
def remove_vote():
    """Remove the user's vote for this article."""

    article_id = request.args.get('article_id')

    if not article_id:
        return redirect(url_for('mod_main.all_feeds'))

    article = FeedArticle.query.get(article_id)
    if not article:
        abort(404)
    else:
        vote = FeedVote.query.get((user_id, article_id))
        if vote:
            if vote.is_upvote:
                article.upvote -= 1
            else:
                article.downvote -= 1
            article.update_wilson_score()
            db.session.delete(vote)

    return jsonify({
        'article_id': article_id,
        'downvote': article.downvote,
        'upvote': article.upvote})

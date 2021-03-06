from flask import (render_template,
                   abort,
                   redirect,
                   jsonify,
                   request,
                   url_for)
from flask.ext.login import login_required, current_user

from app import db
from app.mod_feed import mod_feed
from app.models import FeedArticle, FeedVote


@mod_feed.route('/article')
def read_article():
    """View the readable content of the article."""

    article_id = request.args.get('article_id')
    if not article_id:
        return render_template(url_for('mod_feed.index'))

    article = FeedArticle.query.get(article_id)
    if not article:
        abort(404)

    related_articles = []
    for docid in article.get_related_articles():
        doc = FeedArticle.query.get(docid)
        if doc:
            related_articles.append({
                'title': doc.title,
                'link': doc.link})

    formatted_article = {
        'title': article.title,
        'link': article.link,
        'readable': article.html_readable,
        'related_articles': related_articles}

    return render_template('read.html', article=formatted_article)


@mod_feed.route('/upvote')
@login_required
def upvote():
    """Increase the vote of the article."""

    article_id = request.args.get('article_id')

    if not article_id:
        return redirect(url_for('mod_main.all_feeds'))

    article = FeedArticle.query.get(article_id)
    if not article:
        abort(404)

    vote = FeedVote.query.get((current_user.id, article_id))

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

    return redirect(url_for('mod_feed.index'))


@mod_feed.route('/downvote')
@login_required
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

    return redirect(url_for('mod_feed.index'))


@mod_feed.route('/remove_vote')
@login_required
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

    return redirect(url_for('mod_feed.index'))

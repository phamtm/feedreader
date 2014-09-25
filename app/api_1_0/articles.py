from flask import abort, jsonify, request

from app.api_1_0 import api
from app.models import FeedArticle


@api.route('/article/get', methods=['GET', 'POST'])
def get_article():
    article_id = request.args.get('article_id', type=int)
    if not article_id:
        abort(404)

    article = FeedArticle.query.get(article_id)

    if not article:
        abort(404)

    return jsonify({
        'title': article.title,
        'thumbnail_url': article.thumbnail_url,
        'summary': article.summary})


@api.route('/article/add_to_magazine', methods=['GET', 'POST'])
def add_to_magazine():
    article_id = request.args.get('article_id', type=int)
    magazine_id = request.args.get('magazine_id', type=int)

    if not article_id or not magazine_id:
        abort(404)

    if not FeedArticle.query.get(article_id):
        abort(404)

    magazine = Magazine.query.filter_by(
        user_id=current_user.id,
        id=magazine_id).first()

    if not magazine:
        abort(404)

    res = magazine.add_article(article_id)
    if res:
        flash('article saved')
    else:
        flash('article not saved')

    return redirect(url_for('mod_feed.feeds_from_source', source_id=1))


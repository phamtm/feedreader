from flask import abort, g, jsonify

from app.api_1_0 import api
from app.models import Magazine


@api.route('/magazine/list_magazines')
def list_magazines():
    """View the current user's magazines."""
    magazines = Magazine.query.filter_by(user_id=g.current_user.id).all()

    magazines_json = [m.to_json() for m in magazines]
    response = jsonify({'magazines':magazines_json})
    return response


@api.route('/magazine/add_article')
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

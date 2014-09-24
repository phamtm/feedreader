from flask import render_template

from app.decorators import permission_required
from app.mod_admin import mod_admin
from app.models import FeedArticle, Permission


@permission_required(Permission.ADMIN)
def admin():
    """The admin panel."""
    return 'hello admin'


@permission_required(Permission.ADMIN)
@mod_admin.route('/articles')
def list_articles():
	"""List all articles in the database."""
	articles = FeedArticle.query.order_by(FeedArticle.source_id).all()

	return render_template('admin/articles.html', articles=articles)


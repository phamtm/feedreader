from flask import render_template

from app.decorators import permission_required
from app.mod_admin import mod_admin
from app.models import FeedArticle, Permission


@permission_required(Permission.ADMIN)
def admin():
    """The admin panel."""
    return 'hello admin'


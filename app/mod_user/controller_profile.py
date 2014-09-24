from flask import (render_template,
                   flash,
                   request,
                   url_for)

from flask.ext.login import login_required, current_user

from app import db
from app.models import FeedArticle, Magazine, MagazineArticle, User
from app.mod_user import mod_user
from app.forms import CreateMagazineForm

@mod_user.route('/profile')
def profile():
    """View the user profile."""
    user_id = request.args.get('user_id', current_user.id, type=int)

    user = User.query.get(user_id)

    if not user:
        abort(404)

    return render_template('user/profile.html', user=user)


@login_required
@mod_user.route('/magazine')
def list_magazines():
    """View the current user's magazines."""
    magazines = Magazine.query.filter_by(user_id=current_user.id)

    return render_template('magazines/list_magazines.html',
                           magazines=magazines)


@mod_user.route('/magazine/view')
def view_magazine():
    """View the articles saved inside the magazine."""
    magazine_id = request.args.get('magazine_id', type=int)

    magazine = Magazine.query.get(magazine_id)

    if not magazine:
        flash('Magazine does not exist')
        abort(404)

    if not magazine.public and current_user.is_authenticated() and current_user.id != magazine.user_id:
        flash('This magazine is private')
        abort(404)

    return render_template('magazines/view_magazine.html',
                           magazine=magazine)

@login_required
@mod_user.route('/magazine/create', methods=['GET', 'POST'])
def create_magazine():
    form = CreateMagazineForm()

    if form.validate_on_submit():
        magazine = Magazine(user_id=current_user.id,
                            name=form.name.data,
                            public=form.public.data)
        db.session.add(magazine)
        flash('You have successfully created a magazine')

    return render_template('magazines/create_magazine.html', form=form)



@mod_user.route('/magazine/add_article')
def add_to_magazine():
    article_id = request.args.get('article_id', type=int)
    magazine_id = request.args.get('magazine_id', type=int)

    if not article_id or not magazine_id:
        abort(404)

    magazine = Magazine.query.filter_by(
        user_id=current_user.id,
        id=magazine_id).first()

    if not magazine:
        abort(404)

    # Don't add an existing entry
    magazine.add_article(article_id)
    flash('article saved')

    return render_template('feeds.html')


@mod_user.route('/magazine/remove_article')
def remove_from_magazine():
    article_id = request.args.get('article_id', type=int)
    magazine_id = request.args.get('magazine_id', type=int)

    if not article_id or not magazine_id:
        abort(404)

    magazine = Magazine.query.filter_by(
        user_id=current_user.id,
        id=magazine_id).first()

    if not magazine:
        abort(404)

    # Don't add an existing entry
    magazine.remove_article(article_id)

    return render_template('feeds.html')


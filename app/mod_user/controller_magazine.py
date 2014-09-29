from flask import (abort,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for)
from flask.ext.login import login_required, current_user

from app import db
from app.models import FeedArticle, Magazine, MagazineArticle
from app.mod_user import mod_user
from app.forms import CreateMagazineForm, EditMagazineForm


@mod_user.route('/magazine')
@login_required
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

    if not magazine.public:
        if current_user.is_authenticated():
            if current_user.id != magazine.user_id:
                flash('This magazine is private')
                abort(404)
        else:
            abort(404)

    return render_template('magazines/view_magazine.html',
                           magazine=magazine)


@mod_user.route('/magazine/edit', methods=['GET', 'POST'])
@login_required
def edit_magazine():
    """Edit the preference for this magazine"""
    magazine_id = request.args.get('magazine_id', type=int)
    magazine = None

    if magazine_id:
        magazine = Magazine.query.filter_by(
            id=magazine_id,
            user_id=current_user.id).first()

    if not magazine:
        return redirect(url_for('mod_feed.feeds_from_source'))

    form = EditMagazineForm()

    if form.validate_on_submit():
        magazine.name = form.name.data
        magazine.public = form.public.data

    return render_template('magazines/edit_magazine.html',
                           form=form,
                           magazine=magazine)


@mod_user.route('/magazine/create', methods=['GET', 'POST'])
@login_required
def create_magazine():
    form = CreateMagazineForm()

    if form.validate_on_submit():
        magazine = Magazine(user_id=current_user.id,
                            name=form.name.data,
                            public=form.public.data)
        db.session.add(magazine)
        flash('You have successfully created a magazine')
        return redirect(url_for('mod_user.list_magazines'))

    return render_template('magazines/create_magazine.html', form=form)


@mod_user.route('/magazine/delete')
@login_required
def remove_magazine():
    magazine_id = request.args.get('magazine_id', type=int)

    if not magazine_id:
        abort(404)

    magazine = Magazine.query.filter_by(id=magazine_id,
                                        user_id=current_user.id).first()

    if not magazine:
        abort(404)

    db.session.delete(magazine)

    return redirect(url_for('mod_user.list_magazines'))


@mod_user.route('/magazine/follow')
@login_required
def follow_magazine():
    magazine_id = request.args.get('magazine_id', type=int)

    if not magazine_id:
        abort(404)

    magazine = Magazine.query.get(magazine_id)


@mod_user.route('/magazine/add_article')
@login_required
def add_article():
    article_id = request.args.get('article_id', type=int)
    magazine_id = request.args.get('magazine_id', type=int)

    if not article_id or not magazine_id or not FeedArticle.query.get(article_id):
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


@mod_user.route('/magazine/remove_article')
@login_required
def remove_article():
    article_id = request.args.get('article_id', type=int)
    magazine_id = request.args.get('magazine_id', type=int)

    if not article_id or not magazine_id:
        abort(404)

    magazine = Magazine.query.filter_by(
        user_id=current_user.id,
        id=magazine_id).first()

    if not magazine:
        abort(404)

    magazine.remove_article(article_id)

    return redirect(url_for('mod_user.view_magazine', magazine_id=magazine_id))


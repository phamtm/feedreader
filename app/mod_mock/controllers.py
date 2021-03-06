from flask import render_template, url_for, flash
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from app.mod_crawler.parse_article import fetch_html, get_readable
from app.forms import URLForm
from app.mod_mock import mod_mock


@mod_mock.route('/read', methods = ['GET', 'POST'])
def read():
    """Fetch the readable content from an URL."""

    form = URLForm()

    readable = None
    if form.validate_on_submit():
        html = fetch_html(form.url.data)
        readable = get_readable(html, form.url.data)

    return render_template('tests/fetch_article.html', form = form, html_readable = readable)


# Fetch the article's thumbnail
@mod_mock.route('/thumbnail', methods = ['GET', 'POST'])
def thumbnail():
    """Fetch the thumbnail for an URL."""
    form = URLForm()

    thumbnail_url = None
    if form.validate_on_submit():
        # thumbnail_url = fetch_thumbnail(form.url.data)
        pass

    return render_template('tests/fetch_thumbnail.html', form = form, thumbnail_url = thumbnail_url)
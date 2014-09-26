from flask import (redirect,
                   render_template,
                   flash,
                   request,
                   url_for)
from flask.ext.login import current_user, login_required

from app import db
from app.models import FollowUser, Friendship, User
from app.mod_user import mod_user


@mod_user.route('/profile')
def profile():
    """View the user profile."""
    user_id = request.args.get('user_id', current_user.id, type=int)

    user = User.query.get(user_id)
    if not user:
        abort(404)

    return render_template('user/profile.html', user=user)


@mod_user.route('/list_users')
@login_required
def list_users():
    """View the list of all users"""
    users = User.query.filter(User.id!=current_user.id)
    friends = User.query                                    \
        .join(Friendship, User.id == Friendship.user_id2)   \
        .filter(Friendship.user_id1==current_user.id)       \
        .all()

    followers = User.query                          \
        .join(FollowUser, User.id == FollowUser.user_id1)   \
        .filter(FollowUser.user_id2==current_user.id)   \
        .all()

    followings = User.query                         \
        .join(FollowUser, User.id == FollowUser.user_id2)   \
        .filter(FollowUser.user_id1==current_user.id)   \
        .all()

    return render_template(
        'user/list_users.html',
        users=users,
        friends=friends,
        followers=followers,
        followings=followings)


@mod_user.route('/add_friend')
@login_required
def add_friend():
    """Add a friend"""
    user_id = request.args.get('user_id', type=int)

    if user_id:
        current_user.add_friend(user_id)

    return redirect(url_for('mod_user.list_users'))


@mod_user.route('/remove_friend')
@login_required
def remove_friend():
    """Remove a friend"""
    user_id = request.args.get('user_id', type=int)

    if user_id:
        current_user.remove_friend(user_id)

    return redirect(url_for('mod_user.list_users'))


@mod_user.route('/follow_user')
@login_required
def follow_user():
    """FollowUser a user. Followers are not friend with followee"""
    user_id = request.args.get('user_id', type=int)

    if user_id:
        current_user.follow_user(user_id)

    return redirect(url_for('mod_user.list_users'))


@mod_user.route('/unfollow_user')
@login_required
def unfollow_user():
    """Unfollow a user"""
    user_id = request.args.get('user_id', type=int)

    if user_id:
        current_user.unfollow_user(user_id)

    return redirect(url_for('mod_user.list_users'))

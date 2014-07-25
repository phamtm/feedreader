from functools import wraps
from flask import redirect, 	\
				  url_for, 		\
				  abort
from flask.ext.login import current_user
from http_const import HTTP_FORBIDDEN


# Require the user to be unauthenticated. If not redirect to homepage
def unauthenticated_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if current_user.is_authenticated():
			return redirect(url_for('mod_main.index'))
		return f(*args, **kwargs)
	return decorated_function


# Require certains permission to access a function
def permission_required(p):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user.has_permissions(p):
				abort(HTTP_FORBIDDEN)
			return f(*args, **kwargs)
		return decorated_function
	return decorator


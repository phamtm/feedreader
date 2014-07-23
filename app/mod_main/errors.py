from flask import render_template,	\
				  jsonify, 			\
				  request
from app.mod_main import mod_main


@mod_main.app_errorhandler(404)
def page_not_found(e):
	# Respons to api request
	if request.accept_mimetypes.accept_json and \
	   not request.accept_mimetypes.accept_html:
	   resp = jsonify({'error': 'not found'})
	   resp.status_code = 404
	   return resp

	return render_template('errors/404.html'), 404


@mod_main.app_errorhandler(500)
def internal_server_error(e):
	# Respons to api request
	if request.accept_mimetypes.accept_json and \
	   not request.accept_mimetypes.accept_html:
	   resp = jsonify({'error': 'internal server error'})
	   resp.status_code = 500
	   return resp

	return render_template('errors/500.html'), 500


@mod_main.app_errorhandler(403)
def forbidden(e):
	return render_template('errors/403.html'), 500

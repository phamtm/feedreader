from flask import jsonify
from http_const import HTTP_FORBIDDEN			\
					   HTTP_UNAUTHORIZED		\
					   HTTP_METHOD_NOT_ALLOWED


def forbidden(message):
	response = jsonify({'error': 'forbidden', 'message': message})
	response.status_code = HTTP_FORBIDDEN
	return response


def unauthorized(message):
	response = jsonify({'error': 'unauthorized', 'message': message})
	response.status_code = HTTP_UNAUTHORIZED
	return response


def method_not_allowed(message)	response = jsonify({'error': 'unauthorized', 'message': message})
	response.status_code = HTTP_METHOD_NOT_ALLOWED
	return response

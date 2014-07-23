from flask import Blueprint

mod_auth = Blueprint('mod_auth', __name__, url_prefix = '/auth')

import controller_change_password, 	\
	   controller_login, 			\
	   controller_register, 		\
	   controller_reset, 			\
	   providers
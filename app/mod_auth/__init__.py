from flask import Blueprint

mod_auth = Blueprint('mod_auth', __name__, url_prefix='/auth')

import app.mod_auth.controller_change_password,  \
       app.mod_auth.controller_login,            \
       app.mod_auth.controller_register,         \
       app.mod_auth.controller_reset,            \
       app.mod_auth.providers

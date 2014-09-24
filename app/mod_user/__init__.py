from flask import Blueprint

mod_user = Blueprint('mod_user', __name__, url_prefix='/user')

import controller_profile
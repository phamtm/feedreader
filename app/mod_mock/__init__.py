from flask import Blueprint

mod_mock = Blueprint('mod_mock', __name__, url_prefix = '/mock')

import controllers
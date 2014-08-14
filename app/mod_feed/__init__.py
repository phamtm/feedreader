from flask import Blueprint

mod_feed = Blueprint('mod_feed', __name__, url_prefix='/feeds')

import controller_source, controller_user, controller_article

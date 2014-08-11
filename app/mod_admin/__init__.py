from flask import Blueprint

mod_admin = Blueprint(__name__, 'mod_admin', url_prefix='/admin')

import app.mod_admin.controllers

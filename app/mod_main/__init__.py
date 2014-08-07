from flask import Blueprint

mod_main = Blueprint('mod_main', __name__)

import errors
from app.models import Permission

# Context process: make variables globally available to all templates
@mod_main.app_context_processor
def inject_permissions():
	return { 'Permission': Permission }
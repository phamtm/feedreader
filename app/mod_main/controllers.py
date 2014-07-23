# Import flask dependencies
from flask import render_template, 	\
				  flash, redirect,	\
				  url_for, 			\
				  session

# Import the main blue print
from app.mod_main import mod_main

from app.models import Permission

from app.decorators import permission_required


@mod_main.route('/')
def index():
	return render_template('index.html')


@mod_main.route('/admin')
@permission_required(Permission.ADMIN)
def admin():
	return render_template('admin.html')


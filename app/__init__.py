from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.triangle import Triangle

from celery import Celery
from celery.signals import worker_init
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import config
from database import SQLAlchemy


login_manager = LoginManager()
mail = Mail()
celery = Celery()
db = SQLAlchemy()
cdb = SQLAlchemy()

# Endpoint for login page
login_manager.login_view = 'mod_auth.login'


def create_app(config_name='default'):

    # The WSGI application
    app = Flask(__name__)

    # Import the configuration from config object
    app.config.from_object(config[config_name])

    # Initialize extensions
    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    cdb.init_app(app)
    Triangle(app)

    # Async celery database session
    @worker_init.connect
    def initialize_worker_session(signal, sender):
        new_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                                   convert_unicode=True)
        cdb.session.configure(bind=new_engine)

    # Register blueprint
    from app.mod_admin import mod_admin
    from app.api_1_0 import api as api_1_0_blueprint
    from app.mod_auth import mod_auth
    from app.mod_feed import mod_feed
    from app.mod_main import mod_main
    from app.mod_user import mod_user
    app.register_blueprint(mod_admin)
    app.register_blueprint(api_1_0_blueprint)
    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_feed)
    app.register_blueprint(mod_main)
    app.register_blueprint(mod_user)

    if config_name != 'production':
        from mod_mock import mod_mock
        app.register_blueprint(mod_mock)

    return app


def create_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'])

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


app = create_app()
celery = create_celery(app)

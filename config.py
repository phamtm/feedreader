# Define the application directory
import os
from datetime import timedelta


dirname = os.path.dirname(__file__)
basedir = os.path.abspath(dirname)


# The base configuration class that is inherited by others
class Config:
    # Secret key for signing cookies
    SECRET_KEY = 'donttrytoguessmysecretkey' or os.environ.get('SECRET_KEY')

    # Enable protection against Cross Site Request Forgery (CSRF)
    CSRF_ENABLED = True

    # Use a secure, unique key for signing the data
    CSRF_SESSION_KEY = 'csrfhardtoguess'

    # Enable session (cookies) protection
    SESSION_PROTECTION = 'strong'

    # Enable commit after each sql statement
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAX_EMAIL_ADDRESS_LENGTH = 128

    # Confirmation token expiration time: 7 days
    TOKEN_EXPIRATION_TIME = 604800

    # Temporary folder path
    TMP_DIR = os.path.join(basedir, 'tmp')

    # Thumbnails folder path
    THUMBNAIL_DIR = os.path.join(basedir, 'thumbs')

    # Facebook App Key
    FACEBOOK_APP_ID = '273840802804076',
    FACEBOOK_APP_SECRET = '41480f4a41cdcb5d08d2c10d68795421'

    TWITTER_APP_TOKEN = 'B8pegoEf0uNRYhcufCA8SkNh2'
    TWITTER_APP_SECRET = 'StBCTi4EHQYYdxpORXU7QusMgkd41t9IU5S0FkRF2HV0u7f2Q5'

    # Pagination
    ARTICLES_PER_PAGE = 10

    # Celery configuration
    CELERY_BROKER_URL = 'amqp://'
    CELERY_RESULT_BACKEND = 'amqp://'
    CELERY_IMPORTS = ('app.mod_crawler.fetch',
                      'app.mod_crawler.parse_article',
                      'app.mod_crawler.parse_thumbnail')
    CELERY_TIMEZONE = 'UTC'
    CELERYBEAT_SCHEDULE = {
        'update-db-every-thirty-minutes': {
            'task': 'app.mod_crawler.fetch.update_db',
            'schedule': timedelta(seconds=60),
            'args': ()
        },
    }

    # WhooseAlchemy - Full-text search
    WHOOSH_BASE = os.path.join(basedir, 'search.db')


# Development environment configuration
class DevConfig(Config):
    # Enable the development environment
    DEBUG = True

    # Enable verbose mode for sqlalchemy
    # SQLALCHEMY_ECHO = True

    # Development database
    SQLALCHEMY_DATABASE_URI = 'postgresql://minhpham:mac@localhost/feedreader'
    # DATABASE_CONNECT_OPTIONS = {}

    # Email settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMIN_EMAIL = 'admin@foo.bar'

    # Disable any email service,
    NO_SEND_EMAIL = True



# Testing environment configuration
class TestConfig(Config):
    # Diable CSRF protection
    WTF_CSRF_ENABLED = False

    # Test database
    SQLALCHEMY_DATABASE_URI = 'postgresql://minhpham:mac@localhost/feedreader_test'

    # Disable any email service,
    NO_SEND_EMAIL = True

    ADMIN_EMAIL = 'admin@foo.bar'

    SERVER_NAME = 'localhost:5000'



# Production environment configuration
class ProductionConfig(Config):
    # Production database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app-production.sqlite')
    # DATABASE_CONNECT_OPTIONS = {}

    # Disable any email service,
    NO_SEND_EMAIL = False



config = {
    'default': DevConfig,
    'development': DevConfig,
    'test': TestConfig,
    'production': ProductionConfig
}
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Base():
    DEBUG = False
    TESTING = False
    # Turn off flask sqlalchemy track
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # Flask-jwt-extended
    JWT_TOKEN_LOCATION = "headers"
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_SECRET_KEY = "jwt secret"
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_REFRESH_TOKEN_EXPIRES = False
    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"

    # Secret key for signing cookies
    SECRET_KEY = "secret"


class DevelopmentConfig(Base):
    ENV = 'development'
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/catalog-api"


class TestingConfig(Base):
    ENV = 'testing'
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/catalog-api-test"


class ProductionConfig(Base):
    ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/catalog-api"


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

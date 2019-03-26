from configs.base import BaseConfig


class TestingConfig(BaseConfig):
    ENV = 'testing'
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/catalog-api-test"

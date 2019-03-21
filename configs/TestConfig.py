from configs.BaseConfig import BaseConfig


class TestingConfig(BaseConfig):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/catalog-api-test"

from configs.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/catalog-api"

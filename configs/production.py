from configs.base import BaseConfig


class ProductionConfig(BaseConfig):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/catalog-api"

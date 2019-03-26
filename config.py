from configs.development import DevelopmentConfig
from configs.production import ProductionConfig
from configs.test import TestingConfig

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

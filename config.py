from configs.DevConfig import DevelopmentConfig
from configs.ProConfig import ProductionConfig
from configs.TestConfig import TestingConfig

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

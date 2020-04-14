import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    DEBUG = False


class ProductionConfig(Config):
    pass


configDict = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
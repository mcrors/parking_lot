import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    logging.basicConfig(level=logging.DEBUG)


class TestConfig(Config):
    TESTING = True
    DEBUG = False
    logging.basicConfig(level=logging.INFO)


class ProductionConfig(Config):
    logging.basicConfig(level=logging.DEBUG)


configDict = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
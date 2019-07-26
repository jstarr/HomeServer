from homeserver.core.utility import debug_print
import os
debug_print(__name__)

#   Initializations from the environment
env_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                  'sqlite:///homeserver.db')


class Config(object):
    SQLALCHEMY_DATABASE_URI = env_DATABASE_URI


class ProdConfig(object):
    SQLALCHEMY_DATABASE_URI = env_DATABASE_URI


class DevConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = env_DATABASE_URI
        SQLALCHEMY_TRACK_MODIFICATIONS = True
        SWAGGER_UI_JSONEDITOR = True


myConfig = {'development': DevConfig, 'prod': ProdConfig}
debug_print(__name__)

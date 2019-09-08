from homeserver.core.utility import debug_print
import os
debug_print(__name__)


class Config(object):
    '''Initializations from the environment'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                    'sqlite:///homeserver.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
                                    'SQLALCHEMY_TRACK_MODIFICATIONS') or True
    SWAGGER_UI_JSONEDITOR = os.environ.get('SWAGGER_UI_JSONEDITOR') or True
    DEBUG = os.environ.get('DEBUG') or True
    env = os.environ.get('FLASK_ENV', 'prod')

    def __repr__(self):
        print(
            f'SQLALCHEMY_DATABASE_URI: {self.SQLALCHEMY_DATABASE_URI}',
            f'\nSECRET_KEY: {self.SECRET_KEY}',
            f'\nSQLALCHEMY_TRACK_MODIFICATIONS:',
            f'{self.SQLALCHEMY_TRACK_MODIFICATIONS}',
            f'\nSWAGGER_UI_JSONEDITOR: {self.SWAGGER_UI_JSONEDITOR}',
            f'\nDEBUG: {self.DEBUG}',
            f'\nenv: {self.env}'
        )


debug_print(__name__)

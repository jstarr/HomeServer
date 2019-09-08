from homeserver.core.utility import debug_print
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
debug_print(__file__)

db = SQLAlchemy()


api = Api(title='HomeServer Data',
          version='0.01',
          description='HomeServer Database Maintenance.',
          ordered=True)

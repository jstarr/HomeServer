from homeserver.core.utility import debug_print
# from flask import Blueprint
from flask_restplus import Api
debug_print(__file__)


api = Api(title='HomeServer Data',
          version='0.01',
          description='HomeServer Database Maintenance.',
          ordered=True)

# blueprint = Blueprint('api', __name__)

n = 0
for ns in api.namespaces:
    n += 1
    print(f'\t\t\t{n}. {ns}')

debug_print(__file__)

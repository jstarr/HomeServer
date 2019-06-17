"""Starting point for our Flask Website"""
from homeserver import app, api
# from .homeserver.models import User, Role
# from .homeserver.models import Vendor, Manufacturer, MicroProcessor
# from .homeserver.models import Board, Component, RawData

ns = api.namespace('api', description='API for Home based IOT Server')


print(__name__)
if __name__ == 'main':
    print('-' * 25 + ' ...Starting... ' + '-' * 25)
    app.run(host="0.0.0.0", port=5000, debug=True)

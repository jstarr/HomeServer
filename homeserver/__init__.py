from homeserver.core.utility import debug_print
from flask import Flask
from homeserver.config import Config
from homeserver.apis import api, db
from homeserver.apis.users.views import ma as ma_users
from homeserver.apis.boards.views import ma as ma_board
from homeserver.apis.rolls.views import ma as ma_roles
# from homeserver.apis.vendor.views import ma as ma_vendors
from datetime import datetime
debug_print(__file__)


def create_app():
    lbs = '-' * 40
    curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{lbs} {curTime} {lbs}')
    debug_print(__file__)
    app = Flask(__name__)
    app.config.from_object(Config)
    debug_print(__file__)

    #   Register the api
    api.init_app(app)

    db.init_app(app)
    ma_users.init_app(app)
    ma_roles.init_app(app)
    ma_board.init_app(app)
    ma_vendors.init_app(app)
    debug_print(__file__)
    return app

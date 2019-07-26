from homeserver.core.utility import debug_print
from flask import Flask
from homeserver.config import myConfig
from homeserver.apis import api
from homeserver.models import db
from homeserver.apis.users.views import ns as ns_user
from homeserver.apis.boards.views import ns as ns_board
import os
from datetime import datetime
debug_print(__file__)


def create_app():
    debug_print(__file__)
    lbs = '#' * 25
    curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{lbs} {curTime} {lbs}')
    debug_print(__file__)
    app = Flask(__name__)
    tildas = '~' * 25
    print(f'{tildas} {app} {tildas}')
    env = os.environ.get('FLASK_ENV', 'prod')
    Config = myConfig[env]
    app.config.from_object(Config)
    # print(f'Dump Config:\n{app.config}')
    debug_print(__file__)

    #   Register the api
    api.init_app(app)

    #   Register the blueprints
    # app.register_blueprint(bp)

    db.init_app(app)
    debug_print(__file__)
    appType = type(app).__name__
    print(f'\t-App class name: {appType}')
    apiType = type(api).__name__
    print(f'\t-Api class name: {apiType}')
    dbType = type(db).__name__
    print(f'\t-DB class name: {dbType}')
    print('\t-app.url_map.iter_urles:')
    print('\t-Blue Prints:')
    # nBp = 0
    # for bp in app.blueprints.values:
    #     nBp += 1
    #     print(f'\t\t{nBp}.')
    print(f'\t-Blueprints: {app.blueprints.values}')
    print(f'\t-Instance Path: {app.instance_path}')
    print(f'\t-Root Path: {app.root_path}')
    print(f'\t-App Name: {app.name}')
    print(f'\t-App Static URL Path: {app.static_url_path}')

    print('\nAPI Stuff:')
    print(f'\t-Title: {api.title}')
    print(f'\t-URLs: {api.urls}')

    print(f'\tComplete URL: {api._complete_url}')

    print(f"URL's")
    # line = 0
    # for rules in app.url_map.iter_rules():
    #     print(f'\t\tRule: {rules.rule} = {rules.methods}')
    debug_print(__file__)
    return app
    debug_print(__file__)

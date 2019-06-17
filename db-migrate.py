from homeserver import app, db
# from flask import Flask
from homeserver import db
from homeserver.models import User, Role
from homeserver.models import Vendor, Manufacturer, MicroProcessor
from homeserver.models import Board, Component, RawData
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

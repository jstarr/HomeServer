"""Set up a migration from the old database schema to changes"""
from homeserver import app, db
# from flask import Flask
from homeserver.models import *
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

'''To migrate the database, move to the homeserver subdirectory
    then run the following commands:
    > python ../db-migrate.py db init -- creates the migrations folder
    > python ../db-migrate.py db migrate
    > python ../db-migrate.py db upgrade
'''

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

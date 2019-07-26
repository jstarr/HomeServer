from homeserver import app, db
from homeserver.models import User, Role
from homeserver.models import Vendor, Manufacturer, Ucontroller
from homeserver.models import Board, Component, RawData
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role,
                Vendor=Vendor, Manufacturer=Manufacturer,
                Ucontroller=Ucontroller,
                Board=Board, Component=Component, RawData=RawData)

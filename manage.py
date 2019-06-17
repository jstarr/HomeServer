from HomeServer import app, db
from .models import User, Role
from .models import Vendor, Manufacturer, MicroProcessor
from .models import Board, Component, RawData
from flask_migrate import Migrate

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role,
                Vender=Vendor, Manufacturer=Manufacturer,
                MicroProcessor=MicroProcessor,
                Board=Board, Component=Component, RawData=RawData)

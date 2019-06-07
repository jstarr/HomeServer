from HomeServer import app, db
from .models import User, Role, Board, Component, BoardComponent
from .models import Manufacturer, Vendor, RawData


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Board=Board,
                Component=Component, BoardComponent=BoardComponent,
                Manufacturer=Manufacturer, Vender=Vendor, RawData=RawData)

"""The models for our database data."""

from homeserver.core.utility import debug_print
from datetime import datetime
import secrets
from homeserver.apis import db
debug_print(__file__)

nBase = 12


def spaces(nBase, prompt):
    nSpaces = '.' * (nBase - len(prompt))
    return f'{prompt}: {nSpaces} '


class User(db.Model):
    """The user is only useful for the website, not the api."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roll_id = db.Column(db.Integer)
    reset_token = db.Column(db.Text(), nullable=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        fUser = f'\n\t{spaces(nBase, "Id")} {self.id}'
        fName = f'\n\t{spaces(nBase, "Name")} {self.name}'
        fEmail = f'\n\t{spaces(nBase, "Email")} {self.email}'
        fRollID = f'\n\t{spaces(nBase, "Roll_id")} {self.roll_id}'
        fUpd = f'\n\t{spaces(nBase, "Updated")} {self.updated}'
        return ('User:' + fUser + fName + fEmail + fRollID + fUpd)

    def get_reset_token(self):
        self.reset_token = secrets.token_hex(16)
        return self.reset_token

    @staticmethod
    def verify_reset_token(self, token):
        id = self.query.filter_by(reset_token=token).first()
        return self.query.get(id)


class Role(db.Model):
    """List of valid roles for the users."""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    #   Name of the role.  e.g. 'Admin', 'Maintainer', 'Viewer'
    name = db.Column(db.Text, nullable=False)
    #   Describe the use of the role
    desc = db.Column(db.Text, nullable=True)
    #   Timestamp, last updated
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        fID = f'\n\t{spaces(nBase, "ID")} {self.id}'
        fName = f'\n\t{spaces(nBase, "Name")} {self.name}'
        fDesc = f'\n\t{spaces(nBase, "Desc")} {self.desc}'
        fUpd = f'\n\t{spaces(nBase, "Updated")} {self.updated}'
        return(f'Roles:' + fID + fName + fDesc + fUpd)


class Vendor(db.Model):
    """Where we bought the component or board."""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    street1 = db.Column(db.Text, nullable=True)
    street2 = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(24), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    url = db.Column(db.Text, nullable=True)
    components = db.relationship('Component', backref='vendor', lazy=True)
    boards = db.relationship('Board', backref='vendor', lazy=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        fID = f'\n\t{spaces(nBase, "Id")} {self.id}'
        fID = f'\n\t{spaces(nBase, "Id")} {self.id}'
        fName = f'\n\t{spaces(nBase, "Name")} {self.name}'
        fStr = f'\n\t{spaces(nBase, "Street")} {self.street1}'
        if (self.street2 != ''):
            fStr += f'Street:\n\t{spaces(nBase, "Street")} {self.street2}'
        fCity = f'\n\t{spaces(nBase, "City")} {self.city}'
        fSt = f'\n\t{spaces(nBase, "State")} {self.state}'
        fZip = f'\n\t{spaces(nBase, "Zip")} {self.zip}'
        fCoun = f'\n\t{spaces(nBase, "Country")} {self.country}'
        fUpd = f'\n\t{spaces(nBase, "Updated")} {self.updated}'
        return('Vendor:'
               + fID + fName + fStr + fCity + fSt + fZip + fCoun + fUpd
               )


class Manufacturer(db.Model):
    """A list of manufacturers and their contacts"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    street1 = db.Column(db.Text, nullable=True)
    street2 = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(24), nullable=True)
    url = db.Column(db.Text, nullable=True)
    boards = db.relationship('Board', backref='manufacturer', lazy=True)
    components = db.relationship('Component', backref='manufacturer',
                                 lazy=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        fID = f'\n\t{spaces(nBase, "Id")} {self.id}'
        fName = f'\n\t{spaces(nBase, "Name")} {self.name}'
        fStr = f'\n\t{spaces(nBase, "Street")} {self.street1}'
        if self.street2 != '':
            fStr += f' {self.street2}'
        fCity = f'\n\t{spaces(nBase, "City")} {self.city}'
        fSt = f'\n\t{spaces(nBase, "State")} {self.state}'
        fZip = f'\n\t{spaces(nBase, "Zip")} {self.zip}'
        fCoun = f'\n\t{spaces(nBase, "Country")} {self.country}'
        fUpd = f'\n\t{spaces(nBase, "Updated")}{self.updated}'
        return('Manufacturer:'
               + fID + fName + fStr + fCity + fSt + fZip + fCoun + fUpd
               )


class Ucontroller(db.Model):
    """Type of processor that you might find on a board"""
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    type = db.Column(db.String(25), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    #   URL documenting the microcontroller
    url = db.Column(db.Text, nullable=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    boards = db.relationship('Board', backref='ucontroller', lazy=True)

    def __repr__(self):
        # sUpd = func.to_char(self.updated, "%m/%d/%Y, %H:%M:%S")
        fID = f'\n\t{spaces(nBase, "ID")} {self.id}'
        fDesc = f'\n\t{spaces(nBase, "Desc")} {self.desc}'
        fURL = f'\n\t{spaces(nBase, "URL")} {self.url}'
        fUpd = f'\n\t{spaces(nBase, "Updated")}{self.updated}'
        return (f"Ucontroller: " + fID + fDesc + fURL + fUpd)


class Board(db.Model):
    """Keep a list of the valid boards with their location."""
    """A board includes a Ucontroller (microcontroler)"""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    desc = db.Column(db.Text, nullable=True)
    ucontroller_id = db.Column(db.Integer,
                               db.ForeignKey('ucontroller.id'),
                               nullable=False)
    #   Each board should have its own security value
    secret = db.Column(db.String(64), nullable=False)
    #   Primary location designation.  For the home, "in" or "out" doors
    prime_location = db.Column(db.String(3), nullable=True)
    #   location once the board is used - For example: bedroom #1
    location = db.Column(db.String(50), nullable=True)
    #   sub_location - where in the location, for example: near window
    sub_location = db.Column(db.String(20), nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)
    #   Boards are bought from vendors and made by manufacturer
    vendor_id = db.Column(db.Integer,
                          db.ForeignKey('vendor.id'),
                          nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'),
                                nullable=True)
    # You can put many components on a board
    components = db.relationship('Component', backref='board',
                                 lazy=True)

    def __repr__(self):
        fID = f'\n\t{spaces(nBase, "ID")} {self.id}'
        fDesc = f'\n\t{spaces(nBase, "Desc")} {self.desc}'
        list1 = [self.prime_location, self.location, self.sub_location]
        location = '/'.join(filter(None, list1))
        fbLoc = f'\n\t{spaces(nBase, "Location")} {location}\t'
        fActive = 'Yes' if self.active else 'No'
        fbActive = f'\n\t{spaces(nBase, "Active")} {fActive}'
        fUpd = f'\n\t{spaces(nBase, "Updated")} {self.updated}'
        return (f"Board:" + fID + fDesc + fbLoc + fbActive + fUpd)


class Component(db.Model):
    """List of available components and a little info about them."""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120))
    purpose = db.Column(db.String(120))
    url = db.Column(db.Text, nullable=True)
    manufacturer_id = db.Column(db.String(64),
                                db.ForeignKey('manufacturer.id'),
                                nullable=False)
    #   Vendor id where the component was purchased
    vendor_id = db.Column(db.Integer,
                          db.ForeignKey('vendor.id'),
                          nullable=False)
    price_paid = db.Column(db.Float, nullable=True)
    date_purchased = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)
    #   Once placed on a board, enter the following data
    board_id = db.Column(db.Integer,
                         db.ForeignKey('board.id'),
                         nullable=False)
    pin_no = db.Column(db.Integer, nullable=True)
    MQTT_topic = db.Column(db.String(120), nullable=True)
    data = db.relationship('RawData', backref='component', lazy=True)
    usage = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        fID = f'\n\t{spaces(nBase, "ID")} {self.id}'
        fName = f'\n\t{spaces(nBase, "Name")} {self.name}'
        fPur = f'\n\t{spaces(nBase, "Purpose")} {self.purpose}'
        manName = None if self.manufacturer is None else self.manufacturer.name
        fMan = f'\n\t{spaces(nBase, "Manuf")} {manName}'
        venName = None if self.vendor is None else self.vendor.name
        fVen = f'\n\t{spaces(nBase, "Vendor")} {venName}'
        fPrice = f'\n\t{spaces(nBase, "Price")} {self.price_paid}'
        fPDate = f'\n\t{spaces(nBase, "Purchased")} {self.date_purchased}'
        fPin = f'\n\t{spaces(nBase, "Pin No")} {self.pin_no}'
        fTopic = f'\n\t{spaces(nBase, "MQTT Topic")} {self.MQTT_topic}'
        fUsage = f'\n\t{spaces(nBase, "Usage")} {self.usage}'
        fActive = f'\n\t{spaces(nBase, "Active")} {self.active}'
        fUpd = f'\n\t{spaces(nBase, "Updated")} {self.updated}'
        return (
            'Component:' + fID + fName + fPur + fMan + fVen + fPrice +
            fPDate + fPin + fTopic + fUsage + fActive + fUpd
        )


class RawData(db.Model):
    """The actual data readings from the components."""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    #   Time of measurement.  Should not be changed
    time_stamp = db.Column(db.DateTime, default=datetime.now())
    #   Measurement value
    value = db.Column(db.Text, nullable=False)
    #   May want to add a note to a measurement
    note = db.Column(db.Text, nullable=True)
    #   Should very rarely be changed, but if there is a reason to update this
    #   record, document the time of change here
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    creator = db.Column(db.Integer, db.ForeignKey('component.id'),
                        nullable=True)

    def __repr__(self):
        fID = f'\n\t{spaces(nBase, "Id")} {self.id}'
        fVal = f'\n\t{spaces(nBase, "Value")} {self.value}'
        fNotes = f'\n\t{spaces(nBase, "Notes")} {self.note}'
        fBID = f'\n\t{spaces(nBase, "Board ID")} {self.board.desc}'
        fComID = f'\n\t{spaces(nBase, "Component ID")} {self.component.name}'
        fUpd = f'\n\t{spaces(nBase, "Updated")} {self.updated}'
        return('Data:'
               + fID + fVal + fNotes + fBID + fComID + fUpd
               )


debug_print(__file__)

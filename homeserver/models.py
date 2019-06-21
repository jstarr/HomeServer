"""The models for our database data."""

from datetime import datetime
import secrets
from homeserver import db


class User(db.Model):
    """The user is only useful for the website, not the api."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roll_id = db.Column(db.Integer)
    reset_token = db.Column(db.Text(), nullable=True)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        fUser = f'Users\t\tId:\t\t{self.id}'
        fName = f'\t\tName:\t\t{self.name}'
        fEmail = f'\t\tEmail:\t\t{self.email}'
        fRollID = f'\t\tRoll_id:\t{self.roll_id}'
        fUpd = f'\t\tUpdated:\t{self.updated}'
        return (fUser + fName + fEmail + fRollID + fUpd)

    def get_reset_token(self):
        self.reset_token = secrets.token_hex(16)
        return self.reset_token

    @staticmethod
    def verify_reset_token(self, token):
        try:
            user_id = self.query.filter_by(reset_token=token).first()
        except:
            return None
        return self.query.get("user_id")


class Role(db.Model):
    """List of valid roles for the users."""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    #   Name of the role.  e.g. 'Admin', 'Maintainer', 'Viewer'
    name = db.Column(db.Text, nullable=False)
    #   Describe the use of the role
    desc = db.Column(db.Text, nullable=True)
    #   Timestamp, last updated
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())

    def __repr__(self):
        fID = f'\t\tID:\t\t{self.id}'
        fName = f'\t\tName:\t\t{self.name}'
        fDesc = f'\t\tDesc:\t\t{self.desc}'
        fUpd = f'\t\tUpdated:\t{self.updated}'
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
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        fID = f'\t\tID:\t\t{self.id}'
        fName = f'\t\tName:\t\t{self.name}'
        fStr = f'\t\tStreet:\t\t{self.street1}'
        if (self.street2 != ''):
            fStr += f' Street:\t\t{self.street2}'
        fCity = f'\t\tCity:\t\t{self.city}'
        fSt = f'\t\tState:\t\t{self.state}'
        fZip = f'\t\tZip:\t\t{self.zip}'
        fCoun = f'\t\tCountry:\t\t{self.country}'
        fUpd = f'\t\tUpdated:\t{self.updated}'
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
    components = db.relationship('Component', backref='manufacturer', lazy=True)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())

    def __repr__(self):
        fID = f'\t\tID:\t\t{self.id}'
        fName = f'\t\tName:\t\t{self.name}'
        fStr = f'\t\tStreet:\t\t{self.street1}'
        if self.street2 != '':
            fStr += f' {self.street2}'
        fCity = f'\t\tCity:\t\t{self.city}'
        fSt = f'\t\tState:\t\t{self.state}'
        fZip = f'\t\tZip:\t\t{self.zip}'
        fCoun = f'\t\tCountry:\t\t{self.country}'
        fUpd = f'\t\tUpdated:\t{self.updated}'
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
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    boards = db.relationship('Board', backref='ucontroller', lazy=True)

    def __repr__(self):
        # sUpd = func.to_char(self.updated, "%m/%d/%Y, %H:%M:%S")
        fID = f'\t\tID:{self.id}'
        fDesc = '\t\tDesc:{self.desc}'
        fUpd = f'\t\tUpdated:\t{self.updated}'
        return (f"Ucontroller: " + fID + fDesc + fUpd)


class Board(db.Model):
    """Keep a list of the valid boards with their location."""
    """A board includes a Ucontroller (microcontroler)"""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    desc = db.Column(db.Text, nullable=True)
    ucontroller_id = db.Column(db.Integer,
                               db.ForeignKey('ucontroller.id'))
    #   Each board should have its own security value
    secret = db.Column(db.String(64), nullable=False)
    #   Primary location designation.  For the home, "in" or "out" doors
    prime_location = db.Column(db.String(3), nullable=True)
    #   location once the board is used - For example: bedroom #1
    location = db.Column(db.String(50), nullable=True)
    #   sub_location - where in the location, for example: near window
    sub_location = db.Column(db.String(20), nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    #   Boards are bought from vendors and made by manufacturer
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    # You can put many components on a board
    components = db.relationship('Component', backref='board',
                                 lazy=True)

    def __repr__(self):
        fID = f'\t\tID:{self.id}'
        fDesc = '\t\tDesc:{self.desc}'
        location = (self.prime_location +
                    '-' + self.location
                    + '-' + self.sub_location)
        fbLoc = f'\t\t{location}\t'
        fUpd = f'\t\tUpdated:\t{self.updated}'
        return (f"Board:" + fID + fDesc + fbLoc + fUpd)


class Component(db.Model):
    """List of available components and a little info about them."""

    component_id = db.Column(db.Integer, primary_key=True, nullable=False)
    component_name = db.Column(db.String(120))
    purpose = db.Column(db.String(120))
    url = db.Column(db.Text, nullable=True)
    manufacturer_id = db.Column(db.String(64),
                                db.ForeignKey('manufacturer.id'))
    #   Vendor id where the component was purchased
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    price_paid = db.Column(db.Float, nullable=True)
    date_purchased = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())
    #   Once placed on a board, enter the following data
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    pin_no = db.Column(db.Integer, nullable=True)
    MQTT_topic = db.Column(db.String(120), nullable=True)
    usage = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        fID = f'\t\tID:\t\t{self.component_id}'
        fName = f'\t\tName:\t\t{self.component_name}'
        fPur = f'\t\tPurpose:\t\t{self.purpose}'
        fMan = f'\t\tManuf:\t\t{self.manufactrure}'
        fVen = f'\t\tVendor:\t\t{self.vendor_id}'
        fPrice = f'\t\tPrice:\t\t{self.price_paid}'
        fPDate = f'\t\tPurchased:\t\t{self.date_purchased}'
        fPin = f'\t\tPin No:\t\t{self.pin_no}'
        fTopic = f'\t\tMQTT Topic:\t\t{self.MQTT_topic}'
        fUsage = f'\t\tUsage:\t\t{self.usage}'
        fActive = f'\t\tActive:\t\t{self.active}'
        fUpd = f'\t\tUpdated:\t{self.updated}'
        return (
            'Component:' + fID + fName + fPur + fMan + fVen + fPrice +
            fPDate + fPin + fTopic + fUsage + fActive + fUpd
        )


''' class BoardComponent(db.Model):
    
    bc_id = db.Column(db.Integer, primary_key=True, nullable=False)
    component_id = db.Column(db.Integer,
                             db.ForeignKey('component.component_id'),
                             nullable=False)
    active = db.Column(db.Boolean, default=False)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())

    def __repr__(self):
        fID = f'\t\tID:\t\t{self.bc_id}'
        fBoard = f'\t\tBoard id:\t\t{self.board_id}'
        fActive = f'\t\tActive:\t\t{self.active}'
        fUpd = f'\t\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
        return('Board Component:' + fID + fBoard + fPin + fTopic + fUsage +
               fActive + fUpd
               ) '''


class RawData(db.Model):
    """The actual data readings from the components."""

    data_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # bc_id = db.Column(db.Integer, nullable=False) # BoardComponent id (obsolete)
    #   Time of measurement.  Should not be changed
    time_stamp = db.Column(db.DateTime, default=datetime.now())
    #   Measurement value
    value = db.Column(db.Text, nullable=False)
    #   May want to add a note to a measurement
    note = db.Column(db.Text, nullable=True)
    #   Should very rarely be changed, but if there is a reason to update this
    #   record, document the time of change here
    updated = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        fID = f'\t\tID:\t\t{self.data_id}'
        # fCom = f'\t\tBoard/Component:\t{self.bc_id}'
        fVal = f'\t\tValue:\t\t{self.value}'
        fNotes = f'\t\tNotes:\t\t{self.note}'
        fBID = f'\t\tBoard ID:\t{self.board_id}'
        fComID = f'\t\tComponent ID:\t{self.component_id}'
        fUpd = f'\t\tUpdated:\t{self.updated}'
        return('Data:'
               + fID + fVal + fNotes + fBID + fComID + fUpd
               )

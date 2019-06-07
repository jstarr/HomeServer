"""The models for our database data."""

from datetime import datetime
import secrets
from HomeServer import db


class User(db.Model):
    """The user is only useful for the website, not the api."""

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roll_id = db.Column(db.Integer)
    reset_token = db.Column(db.Text(), nullable=True)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        fUser = f'Users\n\tId:\t\t{self.user_id}'
        fName = f'\n\tName:\t\t{self.username}'
        fEmail = f'\n\tEmail:\t\t{self.email}'
        fRollID = f'\n\tRoll_id:\t{self.roll_id}'
        fUpd = f'\n\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
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

    role_id = db.Column(db.Integer, primary_key=True, nullable=False)
    #   Name of the role.  e.g. 'Admin', 'Maintainer', 'Viewer'
    role_name = db.Column(db.Text, nullable=False)
    #   Describe the use of the role
    role_desc = db.Column(db.Text, nullable=True)
    #   Timestamp, last updated
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())

    def __repr__(self):
        fID = f'\n\tID:\t\t{self.role_id}'
        fName = f'\n\tName:\t\t{self.role_name}'
        fDesc = f'\n\tDesc:\t\t{self.role_desc}'
        fUpd = f'\n\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
        return(f'Roles:' + fID + fName + fDesc + fUpd)


class Board(db.Model):
    """Keep a list of the valid boards with their location."""

    board_id = db.Column(db.Integer, primary_key=True, nullable=False)
    board_desc = db.Column(db.Text, nullable=True)
    #   board_secret will security for incoming data
    board_secret = db.Column(db.String(64), nullable=False)
    #   location - For example: bedroom #1
    board_location = db.Column(db.String(50), nullable=True)
    #   sub_location - where in the location, for example: near window
    board_sub_location = db.Column(db.String(20), nullable=True)
    #   Is the location indoors (in) or outdoors (out)
    board_in_out = db.Column(db.String(3), nullable=True)
    board_active = db.Column(db.Boolean, nullable=True)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())

    def __repr__(self):
        fID = f'\n\tID:{self.board_id}'
        fDesc = '\n\tDesc:{self.board_desc}'
        fbLoc = f'\n\t{self.board_location}'
        fUpd = f'\n\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
        return (f"Board:" + fID + fDesc + fbLoc + fUpd)


class Component(db.Model):
    """List of available components and a little info about them."""

    component_id = db.Column(db.Integer, primary_key=True, nullable=False)
    component_name = db.Column(db.String(120))
    purpose = db.Column(db.String(120))
    manufacturer = db.Column(db.String(64),
                             db.ForeignKey('manufacturer.manuf_id'))
    board_location = db.Column(db.String(24))
    #   Vendor id where the component was purchased
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.vendor_id'))
    price_paid = db.Column(db.Float, nullable=True)
    date_purchased = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())
    components = db.relationship('BoardComponent', backref='component',
                                 lazy=True)

    def __repr__(self):
        fID = f'\n\tID:\t\t{self.component_id}'
        fName = f'\n\tName:\t\t{self.component_name}'
        fPur = f'\n\tPurpose:\t\t{self.purpose}'
        fMan = f'\n\tManuf:\t\t{self.manufactrure}'
        fLoc = f'\n\tLoc:\t\t{self.board_location}'
        fVen = f'\n\tVendor:\t\t{self.vendor_id}'
        fPrice = f'\n\tPrice:\t\t{self.price_paid}'
        fPDate = f'\n\tPurchased:\t\t{self.date_purchased}'
        fActive = f'\n\tActive:\t\t{self.active}'
        fUpd = f'\n\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
        return (
            'Component:' + fID + fName + fPur + fMan + fLoc + fVen + fPrice +
            fPDate + fActive + fUpd
        )


class BoardComponent(db.Model):

    bc_id = db.Column(db.Integer, primary_key=True, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'),
                         nullable=False)
    component_id = db.Column(db.Integer,
                             db.ForeignKey('component.component_id'),
                             nullable=False)
    pin_no = db.Column(db.Integer, nullable=True)
    MQTT_topic = db.Column(db.String(120), nullable=True)
    usage = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=False)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())

    def __repr__(self):
        fID = f'\n\tID:\t\t{self.bc_id}'
        fBoard = f'\n\tBoard id:\t\t{self.board_id}'
        fPin = f'\n\tPin No:\t\t{self.pin_no}'
        fTopic = f'\n\tMQTT Topic:\t\t{self.MQTT_topic}'
        fUsage = f'\n\tUsage:\t\t{self.usage}'
        fActive = f'\n\tActive:\t\t{self.active}'
        fUpd = f'\n\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
        return('Board Component:' + fID + fBoard + fPin + fTopic + fUsage +
               fActive + fUpd
               )


class Manufacturer(db.Model):
    """A list of manufacturers and their contacts"""
    manuf_id = db.Column(db.Integer, primary_key=True, nullable=False)
    manuf_name = db.Column(db.Text, nullable=False)
    manuf_street = db.Column(db.String(52), nullable=True)
    manuf_city = db.Column(db.String(52), nullable=True)
    manuf_state = db.Column(db.String(2), nullable=True)
    manuf_zip = db.Column(db.String(10), nullable=True)
    manuf_country = db.Column(db.String(24), nullable=True)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())

    def __repr__(self):
        fID = f'\n\tID:\t\t{self.manuf_id}'
        fName = f'\n\tName:\t\t{self.manuf_name}'
        fStr = f'\n\tStreet:\t\t{self.manuf_street}'
        fCity = f'\n\tCity:\t\t{self.manuf_city}'
        fSt = f'\n\tState:\t\t{self.manuf_state}'
        fZip = f'\n\tZip:\t\t{self.manuf_zip}'
        fCoun = f'\n\tCountry:\t\t{self.manuf_country}'
        fUpd = f'\n\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
        return('Manufacturer:'
               + fID + fName + fStr + fCity + fSt + fZip + fCoun + fUpd
               )


class Vendor(db.Model):
    vendor_id = db.Column(db.Integer, primary_key=True, nullable=False)
    vendor_name = db.Column(db.Text, nullable=False)
    vendor_street = db.Column(db.String(52), nullable=True)
    vendor_city = db.Column(db.String(52), nullable=True)
    manuf_state = db.Column(db.String(2), nullable=True)
    vendor_zip = db.Column(db.String(10), nullable=True)
    vendor_country = db.Column(db.String(24), nullable=True)
    vendor_phone = db.Column(db.String(15), nullable=True)
    updated = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())

    def __repr__(self):
        fID = f'\n\tID:\t\t{self.vendor_id}'
        fName = f'\n\tName:\t\t{self.vendor_name}'
        fStr = f'\n\tStreet:\t\t{self.vendor_street}'
        fCity = f'\n\tCity:\t\t{self.vendor_city}'
        fSt = f'\n\tState:\t\t{self.vendor_state}'
        fZip = f'\n\tZip:\t\t{self.vendor_zip}'
        fCoun = f'\n\tCountry:\t\t{self.vendor_country}'
        fUpd = f'\n\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
        return('Vendor:'
               + fID + fName + fStr + fCity + fSt + fZip + fCoun + fUpd
               )


class RawData(db.Model):
    """The actual data readings from the components."""

    data_id = db.Column(db.Integer, primary_key=True, nullable=False)
    bc_id = db.Column(db.Integer, nullable=False)
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
        fID = f'\n\tID:\t\t{self.data_id}'
        fCom = f'\n\tBoard/Component:\t{self.bc_id}'
        fVal = f'\n\tValue:\t\t{self.value}'
        fNotes = f'\n\tNotes:\t\t{self.note}'
        fBID = f'\n\tBoard ID:\t{self.board_id}'
        fComID = f'\n\tComponent ID:\t{self.component_id}'
        fUpd = f'\n\tUpdated:\t{self.updated.strftime("%m/%d/%Y, %H:%M:%S")}'
        return('Data:'
               + fID + fCom + fVal + fNotes + fBID + fComID + fUpd
               )

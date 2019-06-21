from HomeServer import app, db
from .models import User, Role
from .models import Vendor, Manufacturer, Ucontroller
from .models import Board, Component, RawData


mpESP32 = Ucontroller(type='ESP32',
                         desc='ESP32 is a series of low-cost, low-power system on a chip microcontrollers with integrated Wi-Fi and dual-mode Bluetooth.')
db.session.add(mpESP32)
db.session.commit()

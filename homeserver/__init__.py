from flask import Flask
from homeserver.config import DevConfig as Config
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
print('*'*15,'db.engine', db.engine, '*'*15)
api = Api(app, version='0.01', title="Test Restful API",
          description="API for Home based IOT Server")

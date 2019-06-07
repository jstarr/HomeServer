class Config(object):
    pass


class ProdConfig(object):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///homeserver.db'

class Config(object):
    CSRF_ENABLED = True # Cross-site request forgery protection for Flask-WTF
    SECRET_KEY = "nv+v9*+#th$vSZgM_F&7rV%nP+wNfw8e"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI= 'sqlite:///../journals.db'

class LiveConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI= 'postgres://postgres:4be8f5645713e20bb679c6f3cacec32d@dokku-postgres-navigatorsdb:5432/navigatorsdb'

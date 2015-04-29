class Config(object):
    DEBUG = False
    CSRF_ENABLED = True # Cross-site request forgery protection for Flask-WTF
    SECRET_KEY = "nv+v9*+#th$vSZgM_F&7rV%nP+wNfw8e"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

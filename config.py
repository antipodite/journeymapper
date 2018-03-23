import os

class Config(object):
    DEBUG = True
    CSRF_ENABLED = True # Cross-site request forgery protection for Flask-WTF
    SECRET_KEY = "nv+v9*+#th$vSZgM_F&7rV%nP+wNfw8e"
    SQLALCHEMY_DATABASE_URI = "sqlite:///journals.db"

class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = "/var/journeys.db"

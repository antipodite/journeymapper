'''
    App-specific DB models live here, so travelogue data specific database
    code is not dependent on the app and can be used separately
'''
from sqlalchemy import Column, Integer, String
from database.models import Base, Metadata
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base, UserMixin):
    
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.name)

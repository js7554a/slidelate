# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.declarative import declared_attr
from flask import current_app
from application import db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, server_default=db.func.now())
    last_updated = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.current_timestamp())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

class User(BaseModel):
    __tablename__ = 'users'
    #id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return '<Post %r>' % self.username

    def generate_auth_token(self, expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
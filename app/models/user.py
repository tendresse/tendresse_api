from hashlib import sha512
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from . import device, gif, success, tendresse
from .. import db


userwithuser = db.Table('userwithuser',
                          db.Column('user1_id', db.Integer, db.ForeignKey(
                              'user.id'), primary_key=True),
                          db.Column('user2_id', db.Integer, db.ForeignKey(
                              'user.id'), primary_key=True)
                          )


userwithsuccess = db.Table('userwithsuccess',
                          db.Column('user_id', db.Integer, db.ForeignKey(
                              'user.id'), primary_key=True),
                          db.Column('success_id', db.Integer, db.ForeignKey(
                              'success.id'), primary_key=True)
                          )


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=True)
    friends = db.relationship('User',
                               secondary=userwithuser,
                               primaryjoin=(userwithuser.c.user1_id == id),
                               secondaryjoin=(userwithuser.c.user2_id == id),
                               backref=db.backref('friended_by', lazy='dynamic'),
                               lazy='dynamic'
    )
    achievements = db.relationship("Success",
                                    secondary=userwithsuccess,
                                    backref=db.backref("users", lazy="dynamic")
    )
    devices = db.relationship("Device",
                              backref=db.backref('user', lazy='joined')
    )

    def generate_auth_token(self, expiration = 172800):
        s = Serializer(current_app.config.get('SECRET_KEY'), expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def get_user_by_token(token):
        s = Serializer(current_app.config.get('SECRET_KEY'), expires_in = 172800)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def verify_password(username_or_token, password):
      # first try to authenticate by token
      user = User.verify_auth_token(username_or_token)
      if not user:
          # try to authenticate with username/password
          user = User.query.filter_by(username = username_or_token).first()
          if not user or not user.verify_password(password):
              return False
      return user

    def __repr__(self):
        return 'User {}>'.format(self.id)

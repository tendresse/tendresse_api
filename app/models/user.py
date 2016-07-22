from .. import db
from hashlib import sha512
from . import token, gif, success, tendresse
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


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
    token = db.Column(db.String)

    def generate_auth_token(self, expiration = 3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        
        return user

    def __repr__(self):
        return 'User {}>'.format(self.id)

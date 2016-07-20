from .. import db
from hashlib import sha512
from . import token, gif, success

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

userwithgif = db.Table('userwithgif',
                          db.Column('user_id', db.Integer, db.ForeignKey(
                              'user.id'), primary_key=True),
                          db.Column('gif_id', db.Integer, db.ForeignKey(
                              'gif.id'), primary_key=True)
                          )

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=True)
    friends = db.relationship('User',
                               secondary=userwithuser,
                               primaryjoin=(userwithuser.c.user1_id == id),
                               secondaryjoin=(userwithuser.c.user2_id == id),
                               backref=db.backref('friended_by', lazy='dynamic'),
                               lazy='dynamic')
    achievements = db.relationship(
        "Success",
        secondary=userwithsuccess,
        backref=db.backref("users", lazy="dynamic")
    )
    tokens = db.relationship(
        "Token",
        backref=db.backref('user', lazy='joined')
    )
    pending = db.relationship(
        "Gif",
        secondary=userwithgif,
        backref=db.backref("users_pending", lazy="dynamic")
    )

    def __repr__(self):
        return 'User {}>'.format(self.id)

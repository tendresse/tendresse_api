from .. import db
from hashlib import sha512

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
    friends = db.relationship(
        "User",
        secondary=userwithuser,
        backref=db.backref("friended", lazy="dynamic")
    ) 
    achievements = db.relationship(
        "Success",
        secondary=userwithsuccess,
        backref=db.backref("users", lazy="dynamic")
    )
    tokens = relationship("Token")
    pending = db.relationship(
        "Gif",
        secondary=userwithgif,
        backref=db.backref("users_pending", lazy="dynamic")
    ) 

    def __repr__(self):
        return 'User {}>'.format(self.id)


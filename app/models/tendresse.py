from .. import db
from . import user, gif


class Tendresse(db.Model):

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    gif_id = db.Column(db.Integer, db.ForeignKey('gif.id'), primary_key=True)
    state_viewed = db.Column(db.Boolean, default=False)
    sender = db.relationship('User',
                              foreign_keys=[sender_id],
                              backref=db.backref("tendresses_sent",
                              remote_side=[sender_id],
                              lazy='dynamic')
                            )
    receiver = db.relationship('User',
                                foreign_keys=[receiver_id],
                                backref=db.backref("tendresses_received",
                                remote_side=[receiver_id],
                                lazy='dynamic')
                              )
    gif = db.relationship('Gif',
                          backref=db.backref("tendresses",lazy='dynamic'))

from .. import db

class Tendresse(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gif_id = db.Column(db.Integer, db.ForeignKey('gif.id'), nullable=False)
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
    
    def matches_any(self,tags):
      for tag in tags:
        if tag in self.tags:
          return True
      return False

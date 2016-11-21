from .. import db

class Tendresse(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    gif_id = db.Column(db.Integer, db.ForeignKey('gif.id'), nullable=False)
    message = db.Column(db.String, default='')
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state_viewed = db.Column(db.Boolean, default=False)
    # backrefs
    gif = db.relationship('Gif',
                          backref=db.backref("tendresses",lazy='dynamic'))
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

    def matches_any(self,tags):
      for tag in tags:
        if tag in self.gif.tags:
          return True
      return False

    def serialize(self):
        d = {}
        d["id"]=self.id
        d["sender"]=self.sender.username
        d["gif"]=self.gif.url
        if self.message is not '':
          d["message"]=self.message
        return d

from .. import db


class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    token = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    platform = db.Column(db.String, nullable=False)

    def __repr__(self):
        return 'Device {}>'.format(self.id)
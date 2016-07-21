from .. import db


class Success(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    title = db.Column(db.String, )
    tags = db.Column(db.String)
    condition = db.Column(db.Integer)
    icon = db.Column(db.String)

    def __repr__(self):
        return 'Success {}>'.format(self.id)

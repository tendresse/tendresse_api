from .. import db


class Success(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    title = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return 'Success {}>'.format(self.id)

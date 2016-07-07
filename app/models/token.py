from .. import db


class Token(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    number = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    platform = db.Column(db.String, nullable=False)

    def __repr__(self):
        return 'Token {}>'.format(self.id)

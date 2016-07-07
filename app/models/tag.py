from .. import db


class Tag(db.Model):

    name = db.Column(db.String, primary_key=True)
    # Additional fields

    def __repr__(self):
        return 'Tag {}>'.format(self.id)

from .. import db


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    name = db.Column(db.String, unique=True)
    url = db.Column(db.String, unique=True)
    # backrefs
    gifs = db.relationship('Gif',
                          backref=db.backref("blog",cascade="all, delete-orphan",lazy='dynamic'))

    def __repr__(self):
        return 'Tag {}>'.format(self.id)

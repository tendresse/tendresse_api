from .. import db

tagwithgif = db.Table('tagwithgif',
                          db.Column('gif_id', db.Integer, db.ForeignKey(
                              'gif.id'), primary_key=True),
                          db.Column('tag_name', db.String, db.ForeignKey(
                              'tag.name'), primary_key=True)
                          )

class Gif(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    url = db.Column(db.String, nullable=False)
    tags = db.relationship(
        "Tag",
        secondary=tagwithgif,
        backref=db.backref("gifs ", lazy="dynamic")
    )

    def __repr__(self):
        return 'Gif {}>'.format(self.id)

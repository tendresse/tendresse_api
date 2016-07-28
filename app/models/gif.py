from .. import db
from .tag import Tag
import random

gifwithtags = db.Table('gifwithtags',
                      db.Column('gif_id', db.Integer, db.ForeignKey(
                          'gif.id'), primary_key=True),
                      db.Column('tag_id', db.Integer, db.ForeignKey(
                          'tag.id'), primary_key=True)
                      )

class Gif(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    url = db.Column(db.String, nullable=False)
    tags = db.relationship(
        "Tag",
        secondary=gifwithtags,
        backref=db.backref("gifs", lazy="dynamic")
    )
    lame_score = db.Column(db.Integer, default=0)


    def __repr__(self):
        return 'Gif {}>'.format(self.id)


    @staticmethod
    def get_random_gif():
        t = Tag.get_random_tag()
        gifs = Gif.query.filter_by(Gif.tags.any(Tag.id==t.id)).all()
        return random.choice(gifs)

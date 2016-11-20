from .. import db
from .tag import Tag
from sqlalchemy.sql.expression import func

gifwithtags = db.Table('gifwithtags',
                       db.Column('gif_id', db.Integer, db.ForeignKey(
                           'gif.id'), primary_key=True),
                       db.Column('tag_id', db.Integer, db.ForeignKey(
                           'tag.id'), primary_key=True)
                       )


class Gif(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    score = db.Column(db.Integer, default=0)
    url = db.Column(db.String, nullable=False)
    # backrefs
    tags = db.relationship(
        "Tag",
        secondary=gifwithtags,
        backref=db.backref("gifs", lazy="dynamic")
    )

    def __repr__(self):
        return 'Gif {}>'.format(self.id)

    @staticmethod
    def get_random_gif():
        gif = db.session.query(Gif).join(Gif.tags).filter(
            Tag.id == Tag.get_random_tag().id).order_by(func.random()).first()
        if gif is not None:
            return gif
        return Gif.get_random_gif()

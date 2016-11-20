from .. import db
from  sqlalchemy.sql.expression import func


class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    banned = db.Column(db.Boolean, default=False)
    # Additional fields

    def __repr__(self):
        return 'Tag {}>'.format(self.id)

    @staticmethod
    def get_random_tag():
        return db.session.query(Tag).order_by(func.random()).first()

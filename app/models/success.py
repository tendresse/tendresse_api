from .. import db

successwithtags = db.Table('successwithtags',
                    db.Column('success_id', db.Integer, db.ForeignKey(
                        'success.id'), primary_key=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey(
                        'tag.id'), primary_key=True)
                  )

class Success(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    title = db.Column(db.String, unique=True )
    tags = db.relationship(
        "Tag",
        secondary=successwithtags,
        backref=db.backref("achievements", lazy="dynamic")
    )
    condition = db.Column(db.Integer)
    type_of = db.Column(db.String)
    icon = db.Column(db.String)

    def __repr__(self):
        return 'Success {}>'.format(self.id)

    def matches_any(self,tags):
      for tag in tags:
        if tag in self.tags:
          return True
      return False

from .. import db

achievementwithtags = db.Table('achievementwithtags',
                    db.Column('achievement_id', db.Integer, db.ForeignKey(
                        'achievement.id'), primary_key=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey(
                        'tag.id'), primary_key=True)
                  )

class Achievement(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    condition = db.Column(db.Integer)
    icon = db.Column(db.Text)
    title = db.Column(db.String, unique=True )
    type_of = db.Column(db.String)
    xp = db.Column(db.Integer)
    # backrefs
    tags = db.relationship(
        "Tag",
        secondary=achievementwithtags,
        backref=db.backref("achievements", lazy="dynamic")
    )
    def __repr__(self):
        return 'Achievement {}>'.format(self.id)

    def matches_any(self,tags):
      for tag in tags:
        if tag in self.tags:
          return True
      return False

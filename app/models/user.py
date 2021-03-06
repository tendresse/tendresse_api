from hashlib import sha512
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from .gif import Gif
from .success import Success
from .tendresse import Tendresse
from .. import db
import requests


userwithuser = db.Table('userwithuser',
                          db.Column('user1_id', db.Integer, db.ForeignKey(
                              'user.id'), primary_key=True),
                          db.Column('user2_id', db.Integer, db.ForeignKey(
                              'user.id'), primary_key=True)
                          )


userwithsuccess = db.Table('userwithsuccess',
                          db.Column('user_id', db.Integer, db.ForeignKey(
                              'user.id'), primary_key=True),
                          db.Column('success_id', db.Integer, db.ForeignKey(
                              'success.id'), primary_key=True)
                          )


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    friends = db.relationship('User',
                               secondary=userwithuser,
                               primaryjoin=(userwithuser.c.user1_id == id),
                               secondaryjoin=(userwithuser.c.user2_id == id),
                               backref=db.backref('friended_by', lazy='dynamic'),
                               lazy='dynamic'
    )
    achievements = db.relationship("Success",
                                    secondary=userwithsuccess,
                                    backref=db.backref("users", lazy="dynamic")
    )
    device = db.Column(db.String)
    role = db.Column(db.String)

    def generate_auth_token(self, expiration = 172800):
        s = Serializer(current_app.config.get('SECRET_KEY'), expires_in = expiration)
        return s.dumps({ 'id': self.id })

    def notify(self, username):
        if self.device != '':
            data = dict()
            data["tokens"] = [self.device]
            data["profile"] = "app"
            data["notification"] = dict()
            data["notification"]["title"] = "new tendresse"
            data["notification"]["message"] = "new tendresse"
            data["notification"]["android"] = dict()
            data["notification"]["android"]["title"] = "new tendresse from "+username
            data["notification"]["android"]["message"] = "launch the app to see it !"
            data["notification"]["ios"] = dict ()
            data["notification"]["ios"]["title"] = "new tendresse from "+username
            data["notification"]["ios"]["message"] = "launch the app to see it !"
            ionic = current_app.config.get('IONIC_API_TOKEN')
            headers = {"Authorization":"Bearer "+ionic,"Content-Type": "application/json"}
            requests.post("https://api.ionic.io/push/notifications",data=data,headers=headers)

    def update_sender_achievements(self):
        sender_achievements = Success.query.filter(Success.type_of == "send").all()
        for achievement in sender_achievements:
          if achievement not in self.achievements:
            if len([k for k in self.tendresses_sent]) >= achievement.condition:
              self.achievements.append(achievement)
        db.session.commit()

    def update_receiver_achievements(self,gif):
        for gif_tag in gif.tags:
          for achievement in gif_tag.achievements:
            if achievement not in self.achievements:
              matching_tendresses = [t for t in self.tendresses_received if t.matches_any(achievement.tags)]
              if len([k for k in matching_tendresses]) >= achievement.condition:
                self.achievements.append(achievement)
        db.session.commit()

    @staticmethod
    def get_user_by_token(token):
        s = Serializer(current_app.config.get('SECRET_KEY'), expires_in = 172800)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def verify_password(username_or_token, password):
      # first try to authenticate by token
      user = User.verify_auth_token(username_or_token)
      if not user:
          # try to authenticate with username/password
          user = User.query.filter_by(username = username_or_token).first()
          if not user or not user.verify_password(password):
              return False
      return user

    def __repr__(self):
        return 'User {}>'.format(self.id)

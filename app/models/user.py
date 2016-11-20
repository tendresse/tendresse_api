from hashlib import sha256
from flask import current_app
from itsdangerous import Serializer, BadSignature
from .gif import Gif
from .achievement import Achievement
from .tendresse import Tendresse
from .. import db, socketio
import requests


userwithuser = db.Table('userwithuser',
                        db.Column('user1_id', db.Integer, db.ForeignKey(
                            'user.id'), primary_key=True),
                        db.Column('user2_id', db.Integer, db.ForeignKey(
                            'user.id'), primary_key=True)
                        )


userwithachievement = db.Table('userwithachievement',
                           db.Column('user_id', db.Integer, db.ForeignKey(
                               'user.id'), primary_key=True),
                           db.Column('achievement_id', db.Integer, db.ForeignKey(
                               'achievement.id'), primary_key=True)
                           )


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    device = db.Column(db.String)
    nsfw = db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)
    premium = db.Column(db.Boolean, default=False)
    role = db.Column(db.String)
    username = db.Column(db.String, nullable=False, unique=True)
    xp = db.Column(db.Integer, default=0)
    # backrefs
    achievements = db.relationship("Achievement",
                                   secondary=userwithachievement,
                                   backref=db.backref("users", lazy="dynamic")
                                   )
    friends = db.relationship('User',
                              secondary=userwithuser,
                              primaryjoin=(userwithuser.c.user1_id == id),
                              secondaryjoin=(userwithuser.c.user2_id == id),
                              backref=db.backref(
                                  'friended_by', lazy='dynamic'),
                              lazy='dynamic'
                              )

    def generate_auth_token(self, expiration=172800):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        return s.dumps({'id': self.id})

    def notify(self, username):
        if self.device != '':
            data = dict()
            data["tokens"] = [self.device]
            data["profile"] = "app"
            data["notification"] = dict()
            data["notification"]["title"] = "new tendresse"
            data["notification"]["message"] = "new tendresse"
            data["notification"]["android"] = dict()
            data["notification"]["android"][
                "title"] = "new tendresse from " + username
            data["notification"]["android"][
                "message"] = "launch the app to see it !"
            data["notification"]["ios"] = dict()
            data["notification"]["ios"][
                "title"] = "new tendresse from " + username
            data["notification"]["ios"][
                "message"] = "launch the app to see it !"
            ionic = current_app.config.get('IONIC_API_TOKEN')
            headers = {"Authorization": "Bearer " +
                       ionic, "Content-Type": "application/json"}
            requests.post("https://api.ionic.io/push/notifications",
                          data=data, headers=headers)

    def update_sender_achievements(self):
        ach = []
        sender_achievements = Achievement.query.filter(
            Achievement.type_of == "send").all()
        for achievement in sender_achievements:
            if achievement not in self.achievements:
                if len([k for k in self.tendresses_sent]) >= achievement.condition:
                    self.achievements.append(achievement)
                    ach.append(achievement)
        db.session.commit()
        return ach

    def update_receiver_achievements(self, gif):
        ach = []
        for gif_tag in gif.tags:
            for achievement in gif_tag.achievements:
                if achievement not in self.achievements:
                    matching_tendresses = [
                        t for t in self.tendresses_received if t.matches_any(achievement.tags)]
                    if len([k for k in matching_tendresses]) >= achievement.condition:
                        self.achievements.append(achievement)
                        ach.append(achievement)
        db.session.commit()
        return ach

    @staticmethod
    def get_user_by_token(token):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def verify_password(username_or_token, password):
        # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = User.query.filter_by(username=username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        return user

    def __repr__(self):
        return 'User {}>'.format(self.id)

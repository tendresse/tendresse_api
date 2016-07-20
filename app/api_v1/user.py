from flask import jsonify, request

from . import api
from .. import db
from ..models.user import User
from ..schemas.user import user_schema, users_schema


@api.route('/users', methods=['GET'])
def get_users():
    pass


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass


@api.route('/users', methods=['POST'])
def signup_user():
    datas = request.get_json()
    username = datas.get('username','')
    password = datas.get('password','').encode('utf-8')
    user = User.query.get(username)
    m = sha512()
    m.update(f.password.data.encode())
    password = m.hexdigest()
    pass


@api.route('/users', methods=['PUT'])
def login_user():
    datas = request.get_json()
    username = datas.get('username','')
    password = datas.get('password','').encode('utf-8')
    user = User.query.get(username)
    m = sha512()
    m.update(f.password.data.encode())
    password = m.hexdigest()
    pass


@api.route('/users/me/disconnect', methods=['GET'])
def disconnect_user():
    pass


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass


# SEND GIF


@api.route('/users/me/send', methods=['POST'])
def submit_gif_user():
    pass


# FRIENDS


@api.route('/users/me/friends', methods=['GET'])
def get_friends_user(id):
    pass


@api.route('/users/me/friends', methods=['POST'])
def add_friend_user():
    pass


@api.route('/users/me/friends', methods=['DELETE'])
def unfriend_user(id):
    pass


# NOTIFICATIONS

@api.route('/users/me/pending', methods=['GET'])
def get_pending_gifs_user(id):
    pass


@api.route('/users/me/pending', methods=['DELETE'])
def remove_notification_user(id):
    pass


# ACHIEVEMENTS


@api.route('/users/me/achievements', methods=['GET'])
def get_achievements_user(id):
    pass

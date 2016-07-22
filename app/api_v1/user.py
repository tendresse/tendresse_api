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
    if not username.isspace():
        if len(username)>3:
            if User.query.filter(User.username == username).first() is None:
                password = datas.get('password','').encode('utf-8')
                if not password.isspace():
                    m = sha512()
                    m.update(password)
                    password = m.hexdigest()
                    device_token = datas.get('device_token','')
                    platform = datas.get('platform','')
                    d = Device(token=device_token,platform=platform)
                    u = User(username=username,password=password)
                    db.session.add(u)
                    db.session.add(d)
                    u.devices.append(d)
                    db.session.commit()
                    token = u.generate_auth_token()
                    u.token = token
                    db.session.commit()
                    return jsonify(state="success",token=token,username=username),200
                else:
                    # invalid password
                    return jsonify(login="password incorrect"),401
            else:
                # username already taken
                return jsonify(state="username already taken"),401
        else:
            # username too short
            return jsonify(login="username too short, 4 characters minimum"),401
    else:
        # invalid username
        return jsonify(login="username incorrect"),401


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

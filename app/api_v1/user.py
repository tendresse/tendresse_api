from flask import jsonify, request, current_app
from hashlib import sha512

from . import api
from .. import db
from ..models.user import User
from ..models.device import Device
from ..schemas.user import user_schema, users_schema
from ..models.success import Success
from ..schemas.success import success_schema, successes_schema



@api.route('/users', methods=['GET'])
def get_users():
    pass


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass

@api.route('/users/devices', methods=['GET'])
def get_devices_by_user():
    datas = request.get_json()
    token = datas.get('token','')
    me = User.verify_auth_token(token)
    if me is not None :
        return users_schema.jsonify(me.devices),200
    return jsonify(state="Current user not found"),403


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
                    return jsonify(token=token.decode('ascii'),username=username),200
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
    if not username.isspace():
        if not password.isspace():
            me = User.query.filter(User.username == username).first()
            if me is not None:
                m = sha512()
                m.update(f.password.data.encode())
                password = m.hexdigest()
                if password == me.password:
                    token = me.generate_auth_token()
                    return jsonify(token=token.decode('ascii'),username=username),200
                else:
                    return jsonify(login="password invalid"),403
            else:
                return jsonify(login="username not found"),404
        else:
            # invalid username
            return jsonify(login="username incorrect"),401
    else:
        # invalid password
        return jsonify(login="password incorrect"),401


    pass

@api.route('/users/me/disconnect', methods=['GET'])
def disconnect_user():
    pass

@api.route('/users/me/reset_token', methods=['PUT'])
def reset_token_user():
    datas = request.get_json()
    token = datas.get('token','')
    me = User.get_user_by_token(token)
    if me:
        token = me.generate_auth_token()
        return jsonify(token=token.decode('ascii')),200
    else:
        return jsonify(state="error token invalid"),401
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
    datas = request.get_json()
    token = datas.get('token','')
    me = User.verify_auth_token(token)
    if me is not None :
        return users_schema.dumps(me.friends),200
    return jsonify(state="Current user not found"),403


@api.route('/users/me/friends', methods=['POST'])
def add_friend_user():
    datas = request.get_json()
    token = datas.get('token','')
    username_friend = datas.get('username_friend','')
    me = User.verify_auth_token(token)
    friend = User.query.filter(User.username == username_friend).first()
    if me is not None :
        if friend not in me.friends:
            me.friends.append(friend)
            db.session.commit()
            return jsonify(state="success",friends=user.friends),200
        return jsonify(state="Friend already added"),401
    return jsonify(state="Current user not found"),403

@api.route('/users/me/friends', methods=['DELETE'])
def unfriend_user():
    datas = request.get_json()
    token = datas.get('token','')
    username_friend = datas.get('username_friend','')
    me = User.verify_auth_token(token)
    friend = User.query.filter(User.username == username_friend).first()
    if me is not None :
        if friend in me.friends:
            me.friends.remove(friend)
            db.session.commit()
            return jsonify(state="success"),200
        return jsonify(state="User not in friends list"),401
    return jsonify(state="Current user not found"),403


# NOTIFICATIONS

@api.route('/users/me/pending', methods=['GET'])
def get_pending_gifs_user(id):
    pass


@api.route('/users/me/pending', methods=['DELETE'])
def remove_notification_user(id):
    pass


# ACHIEVEMENTS


@api.route('/users/me/achievements', methods=['GET'])
def get_achievements_user():
    datas = request.get_json()
    token = datas.get('token','')
    me = User.verify_auth_token(token)
    if me is not None :
        return successes_schema.dumps(me.achievements),200
    return jsonify(state="Current user not found"),403

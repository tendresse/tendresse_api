from flask import jsonify, request, current_app, abort
from hashlib import sha512
from functools import wraps

from . import api
from .. import db
from ..models.device import Device
from ..models.gif import Gif
from ..schemas.gif import gif_schema, gifs_schema
from ..models.user import User
from ..schemas.user import user_schema, users_schema
from ..models.success import Success
from ..schemas.success import success_schema, successes_schema
from ..models.tendresse import Tendresse
from ..schemas.tendresse import tendresse_schema, tendresses_schema


def authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the request header.
    user will be None if the
    authentication failed, and have the User otherwise.

    Usage:
    @app.route("/")
    @authorized
    def secured_root(user=None):
        pass
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            abort(400)
            return None
        token = request.headers['Authorization'].encode('ascii','ignore')
        user = User.get_user_by_token(token)
        if user is None:
            # Unauthorized
            abort(401)
            return None

        return fn(user=user, *args, **kwargs)
    return wrapped


@api.route('/', methods=['GET'])
def get_users():
    return jsonify(state="online"),200



@api.route('/users/<string:username>/profile', methods=['GET'])
def get_user(username):
    user = User.query.filter(User.username == username).first()
    if user is not None:
        return user_schema.jsonify(user),200
    return jsonify(state="user not found"),404



@api.route('/users', methods=['POST'])
def signup_user():
    datas = request.get_json()
    username = datas.get('username','')
    if not username.isspace():
        if len(username)>3:
            if User.query.filter(User.username == username).first() is None:
                password = datas.get('password','').encode('utf-8')
                if not password.isspace() and len(password)>0:
                    m = sha512()
                    m.update(password)
                    password = m.hexdigest()
                    u = User(username=username,password=password)
                    db.session.add(u)
                    device_token = datas.get('device_token','')
                    if device_token!='':
                        platform = datas.get('platform','')
                        d = Device(token=device_token,platform=platform)
                        db.session.add(d)
                        u.devices.append(d)
                    db.session.commit()
                    token = u.generate_auth_token()
                    return jsonify(token=token.decode('ascii'),username=username),200
                else:
                    return jsonify(state="password incorrect"),401
            else:
                return jsonify(state="username already taken"),401
        else:
            return jsonify(login="username too short, 4 characters minimum"),401
    else:
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
                m.update(password)
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

@api.route('/users/me/disconnect', methods=['GET'])
def disconnect_user():
    pass


@api.route('/users/me/reset_token', methods=['GET'])
@authorized
def reset_token_user(user):
    me = user
    token = me.generate_auth_token()
    return jsonify(token=token.decode('ascii')),200


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass


# SEND GIF


@api.route('/users/me/send', methods=['POST'])
@authorized
def submit_gif_user(user):
    me = user
    datas = request.get_json()
    username_friend = datas.get('username_friend', '')
    friend = User.query.filter(User.username == username_friend).first()
    if friend is not None:
        gif = Gif.get_random_gif()
        t = Tendresse(sender_id = me.id, receiver_id = friend.id, gif_id = gif.id)
        db.session.add(t)
        db.session.commit()
        # générer les notifications push
        friend.notify()
        # gérer les achievements
        friend.update_receiver_achievements(gif)
        user.update_sender_achievements()
        return jsonify(state="success"),200
    else:
        return jsonify(state="friend not found"),404


# FRIENDS


@api.route('/users/me/friends', methods=['GET'])
@authorized
def get_friends_user(user):
    return users_schema.jsonify(user.friends), 200


@api.route('/users/me/friends', methods=['POST'])
@authorized
def add_friend_user(user):
    me = user
    datas = request.get_json()
    username_friend = datas.get('username_friend', '')
    friend = User.query.filter(User.username == username_friend).first()
    if friend is not None:
        if friend not in me.friends:
            me.friends.append(friend)
            db.session.commit()
            return jsonify(state="success"), 200
        return jsonify(state="Friend already added"), 401
    return jsonify(state="Friend user not found"), 404


@api.route('/users/me/friends', methods=['DELETE'])
@authorized
def unfriend_user(user):
    me = user
    datas = request.get_json()
    username_friend = datas.get('username_friend', '')
    friend = User.query.filter(User.username == username_friend).first()
    if friend in me.friends:
        me.friends.remove(friend)
        db.session.commit()
        return jsonify(state="success"), 200
    return jsonify(state="User not in friends list"), 401


# NOTIFICATIONS


@api.route('/users/me/pending', methods=['GET'])
@authorized
def get_pending_gifs_user(user):
    pending_tendresses = [t for t in user.tendresses_received if not t.state_viewed]
    return tendresses_schema.jsonify(pending_tendresses)


@api.route('/users/me/pending', methods=['DELETE'])
@authorized
def state_tendresse_as_viewed(user):
    datas = request.get_json()
    tendresse_id = datas.get('tendresse_id', '')
    tendresse = Tendresse.query.get(tendresse_id)
    if tendresse is not None:
        if tendresse.receiver is user:
            tendresse.state_viewed = True
            db.session.commit()
        return jsonify(state="success"),200
    return jsonify(state="tendresse not found"),404


# ACHIEVEMENTS


@api.route('/users/me/achievements', methods=['GET'])
@authorized
def get_achievements_user(user):
    return successes_schema.dumps(user.achievements),200

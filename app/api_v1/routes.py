from flask import jsonify, request, current_app, abort
from hashlib import sha512
from functools import wraps

from . import api
from .. import db
from ..models.user import User


@api.route('/users', methods=['POST'])
def signup_user():
    """ 
    check if username not taken and create an account, returns the corresponding token
    """
    datas = request.get_json()
    username = datas.get('username','').lower()
    if not username.isspace():
        if len(username)>3:
            if User.query.filter(User.username == username).first() is None:
                password = datas.get('password','').encode('utf-8')
                if not password.isspace() and len(password)>0:
                    m = sha512()
                    m.update(password)
                    password = m.hexdigest()
                    device_token = datas.get('device_token','')
                    u = User(username=username,password=password,device=device_token)
                    db.session.add(u)
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
    """ 
    Try to login the user with token, and refresh it if valid
    or try with username/password and create token
    """
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].encode('ascii','ignore')
        user = User.get_user_by_token(token)
        if user is not None:
            token = user.generate_auth_token()
            return jsonify(token=token.decode('ascii'),username=user.username),200
    datas = request.get_json()
    username = datas.get('username','')
    password = datas.get('password','').encode('utf-8')
    if not username.isspace():
        if not password.isspace():
            me = User.query.filter(User.username == username.lower()).first()
            if me is not None:
                m = sha512()
                m.update(password)
                password = m.hexdigest()
                if password == me.password:
                    token = me.generate_auth_token()
                    return jsonify(token=token.decode('ascii'),username=username),200
                else:
                    return jsonify(login="password invalid"),401
            else:
                return jsonify(login="username not found"),404
        else:
            # invalid username
            return jsonify(login="username incorrect"),401
    else:
        # invalid password
        return jsonify(login="password incorrect"),401

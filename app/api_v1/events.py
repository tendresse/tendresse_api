from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect
from .. import socketio
import time

current_user = None

@socketio.on('connect')
def test_connect(token):
    current_user = User.get_user_by_token(token)
    if current_user is None:
    	emit('token invalid',{'state':'error, invalid token'})
    	return False
    print(current_user.username+' connected.')
    join_room(current_user.username)
    emit('connect',{'state':'success'})

@socketio.on('disconnect')
def disconnect():
    print(current_user.username+' disconnected.')
    close_room(current_user.username)
    current_user = None

@socketio.on('get user')
def get_user(username):
    user = User.query.filter(User.username == username.lower()).first()
    if user is not None:
        send(user_schema.jsonify(user))
        emit('get user', jsonify(state="user not found"))

@socketio.on('update device')
def update_device(device_token):
    if device_token != '':
        current_user.device = device_token
        db.session.commit()
        emit('update device',jsonify(state="success"))
    emit('update device',jsonify(state="token invalid"))

@socketio.on('send tendresse')
def send_tendresse(username_friend):
    friend = User.query.filter(User.username == username_friend.lower()).first()
    if friend is not None:
        gif = Gif.get_random_gif()
        t = Tendresse(sender_id = current_user.id, receiver_id = friend.id, gif_id = gif.id)
        db.session.add(t)
        db.session.commit()
        # générer les notifications push
        friend.notify(friend.username)
        # gérer les achievements
        friend.update_receiver_achievements(gif)
        user.update_sender_achievements()
        emit('send tendresse', jsonify(state="success"))
        time.sleep(1)
        emit('new tendresse', t.serialize(), room=friend.username)
    else:
        emit('new tendresse', {"state":"friend not found"})

@socketio.on('get friends')
def get_friends():
    emit('get friends',users_schema.jsonify(current_user.friends))

@socketio.on('add friend')
def add_friend(username_friend):
    friend = User.query.filter(User.username == username_friend).first()
    if friend in current_user.friends:
        current_user.friends.append(friend)
        db.session.commit()
        emit('add friend',{"state":"success"})
    emit('add friend', {"state":"User already in friends list"})

@socketio.on('delete friend')
def unfriend(username_friend):
    friend = User.query.filter(User.username == username_friend).first()
    if friend in current_user.friends:
        current_user.friends.remove(friend)
        db.session.commit()
        emit('delete friend',{"state":"success"})
    emit('delete friend',{"state":"user already in friends list"})

@socketio.on('get tendresses')
def pending():
    pending_tendresses = [t for t in current_user.tendresses_received if not t.state_viewed]
    tendresses_by_user = {}
    for tendresse in pending_tendresses:
        if tendresse.sender.username in tendresses_by_user:
            tendresses_by_user[tendresse.sender.username]["tendresses"].append(tendresse.serialize())
        else:
            tendresses_by_user[tendresse.sender.username]= {}
            tendresses_by_user[tendresse.sender.username]["isFriend"] = tendresse.sender in me.friends
            tendresses_by_user[tendresse.sender.username]["tendresses"] = [tendresse.serialize()]
    emit('get tendresses', jsonify(tendresses_by_user))
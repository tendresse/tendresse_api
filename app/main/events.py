from flask import session, request
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect
from hashlib import sha256
from functools import wraps
import time
# apps
from .. import socketio, db
# models
from ..models.achievement import Achievement
from ..models.blog import Blog
from ..models.gif import Gif
from ..models.tag import Tag
from ..models.tendresse import Tendresse
from ..models.user import User
# schemas
from ..schemas.achievement import achievement_schema, achievements_schema
from ..schemas.blog import blog_schema, blogs_schema
from ..schemas.gif import gif_schema, gifs_schema
from ..schemas.tag import tag_schema, tags_schema
from ..schemas.tendresse import tendresse_schema, tendresses_schema
from ..schemas.user import user_schema, users_schema

###
# TODO :
#   gestion des erreurs plus precises
###

current_user = None

@socketio.on('connect')
def on_connect(token):
    print('an app just connected.')


##################
# WRAPPERS
##################


def authorized(fn):
    """Decorator that checks if current_user is connected
    Usage:
    @app.route("/")
    @authorized
    def secured_root(user=None):
        pass
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if current_user is None:
            return jsonify(success=False, error="you are not connected")
        return fn(*args, **kwargs)
    return wrapped


def admin_only(fn):
    """Decorator that checks if current_user is connected
    Usage:
    @app.route("/")
    @authorized
    def secured_root(user=None):
        pass
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if current_user is not None:
            if current_user.role == 'admin':
                return fn(*args, **kwargs)
            return jsonify(success=False, error="you are not admin")
        return jsonify(success=False, error="you are not connected")
    return wrapped


#########
# USER
#########


@socketio.on('signup')
def signup_user(username, password):
    if not username.isspace():
        if len(username) > 3:
            if User.query.filter( User.username == username.lower() ).first() is None:
                if not password.isspace() and len(password) > 0:
                    m = sha256()
                    m.update(password)
                    password = m.hexdigest()
                    u = User(username=username, password=password)
                    db.session.add(u)
                    db.session.commit()
                    current_user = u
                    token = u.generate_auth_token()
                    print(current_user.username + ' just signed-up.')
                    join_room(current_user.username)
                    return jsonify(success=True, token=token.decode('ascii') )
                else:
                    return jsonify(success=False, error="password incorrect")
            else:
                return jsonify(success=False, error="username already taken")
        else:
            return jsonify(success=False, error="username too short, 4 characters minimum")
    else:
        return jsonify(success=False, error="username incorrect")


@socketio.on('login')
def login_user(username, password):
    if not username.isspace():
        if not password.isspace():
            me = User.query.filter(User.username == username.lower()).first()
            if me is not None:
                m = sha256()
                m.update(password)
                password = m.hexdigest()
                if password == me.password:
                    token = me.generate_auth_token()
                    current_user = me
                    print(current_user.username + ' logged in.')
                    join_room(current_user.username)
                    return jsonify(success=True, token=token.decode('ascii'))
                else:
                    return jsonify(success=False, error="password invalid")
            else:
                return jsonify(success=False, error="username not found")
        else:
            # invalid username
            return jsonify(success=False, error="username incorrect")
    else:
        # invalid password
        return jsonify(success=False, error="password incorrect")


@socketio.on('auth')
def auth(token):
    current_user = User.get_user_by_token(token)
    if current_user is None:
        return False
    print(current_user.username + ' connected with token.')
    join_room(current_user.username)
    return True


@socketio.on('disconnect')
def disconnect():
    print(current_user.username + ' disconnected.')
    close_room(current_user.username)
    current_user = None

@socketio.on('ready')
@authorized
def ready():
    emit('friends' , users_schema.jsonify(current_user.friends) )
    pending_tendresses = [ t for t in current_user.tendresses_received if not t.state_viewed]
    emit('tendresses' , tendresses_schema.jsonify(pending_tendresses) )
    emit('achievements' , successes_schema.jsonify(current_user.achievements) )


@socketio.on('get user')
@authorized
def get_user(username):
    user = User.query.filter(User.username == username.lower()).first()
    if user is not None:
        return user_schema.jsonify(user)
    return False


@socketio.on('update device')
@authorized
def update_device(device_token):
    if current_user is not None:
        current_user.device = device_token
        db.session.commit()
        return True
    return False


#############
# TENDRESSE
#############

@socketio.on('send tendresse')
@authorized
def send_tendresse(username_friend):
    friend = User.query.filter(
        User.username == username_friend.lower()).first()
    if friend is not None:
        gif = Gif.get_random_gif()
        t = Tendresse(sender_id=current_user.id,
                      receiver_id=friend.id, gif_id=gif.id)
        db.session.add(t)
        db.session.commit()
        # générer les notifications push
        friend.notify(friend.username)
        # gérer les achievements
        ach = friend.update_receiver_achievements(gif)
        if ach is not []:
            for a in ach:
                emit('new achievement', success_schema.jsonify(a), room=friend.username)       
        ach = user.update_sender_achievements()
        if ach is not []:
            for a in ach:
                emit('new achievement', success_schema.jsonify(a))  
        emit('new tendresse', t.serialize(), room=friend.username)
        return True
    return False

@socketio.on('tendresse seen')
@authorized
def tendresse_seen(tendresse_id):
    tendresse = Tendresse.query.get(tendresse_id)
    if tendresse is not None:
        if tendresse.receiver is current_user:
            tendresse.state_viewed = True
            db.session.commit()
            return True


##########
# FRIEND
##########


@socketio.on('add friend')
@authorized
def add_friend(username_friend):
    friend = User.query.filter(
        User.username == username_friend.lower()).first()
    if friend is not None:
        if friend in current_user.friends:
            current_user.friends.append(friend)
            db.session.commit()
            print(current_user.username + ' added ' + username_friend + '.')
            return jsonify(success=True)
        return jsonify(success=False, error="user already in friends list")
    return jsonify(success=False, error="user not found")


@socketio.on('delete friend')
@authorized
def unfriend(username_friend):
    friend = User.query.filter(
        User.username == username_friend.lower()).first()
    if friend is not None:
        if friend in current_user.friends:
            current_user.friends.remove(friend)
            db.session.commit()
            return jsonify(success=True)
        return jsonify(success=False, error="user not in friends list")
    return jsonify(success=False, error="user not found")

##########
# ADMIN
##########

@socketio.on('grant user admin')
@admin_only
def user_admin(user_id):
    user = User.query.get(user_id)
    if user is not None:
            user.role = 'admin'
            return jsonify(success=True)
    return jsonify(success=False, error="user not found")


########
# BLOG
########

@socketio.on('get blogs')
@admin_only
def get_blogs():
    return blogs_schema.jsonify(Blog.query.all())

@socketio.on('get blog')
@admin_only
def gifs_from_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog is not None:
        return jsonify(success=True, blog=blog_schema.jsonify(blog))
    return jsonify(success=False, error="blog not found")

@socketio.on('add blog')
@admin_only
def add_blog(blog):
    scheme = blog_schema.load(blog, partial=True)
    known_tags = {}
    avoided_tags = Tag.query.filter(
            Tag.banned == True).all()
    tumblr_key = 'Gm7u68GMu8RCQmIVV1vmr7QlToZ8rYKrzr1HsULlmK0doez73o'
    http = urllib3.PoolManager()
    blog_json_url = "https://api.tumblr.com/v2/blog/"+scheme.data.url+"/posts/photo?api_key="+tumblr_key
    r = http.request('GET', blog_json_url)
    data = json.loads(r.data.decode('utf-8'))
    if data["meta"]["status"] is 200:
        b = Blog(name=scheme.data.name, url=scheme.data.url)
        db.session.add(b)
        total_posts = data["response"]["total_posts"]
        blog_json_url+="&offset="
        for i in range(0,total_posts,50):
            r = http.request('GET', blog_json_url+str(i))
            data = json.loads(r.data.decode('utf-8'))
            for post in data["response"]["posts"]:
                if post["type"] == "photo":
                    for photo in post["photos"]:
                        url_gif = photo["original_size"]["url"]
                        if url_gif[-3:] == "gif":
                            # photo["original_size"]["width"] pour trier si le gif est trop petit ?
                            gif = Gif(url=url_gif)
                            db.session.add(gif)
                            for l_tag in post["tags"]:
                                # sometimes l_tag is a list of tag seperated by blank spaces
                                # so we need to split this string ang get a list of tags
                                l_tag = l_tag.split(' ')
                                for tag in l_tag:
                                    tag = tag.lower()
                                    if not tag.isspace():
                                        if tag not in avoided_tags and len(tag)>2:
                                                if tag not in known_tags :
                                                    o = Tag(name=tag)
                                                    db.session.add(o)
                                                    db.session.commit()
                                                    known_tags[tag] = o
                                                if known_tags[tag] not in gif.tags :
                                                    gif.tags.append(known_tags[tag])
                            db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=True, error="blog invalid or offline")

@socketio.on('delete blog')
@admin_only
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog is not None:
        db.session.delete(blog)
    db.session.commit()

#######
# TAG
#######

@socketio.on('get tags')
@admin_only
def get_tags():
    return tags_schema.jsonify(Tag.query.all())

@socketio.on('get tag')
@admin_only
def get_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag is not None:
        return jsonify(success=True, tag=tag_schema.jsonify(tag))
    return jsonify(success=False, error="tag not found")

@socketio.on('add tag')
@admin_only
def add_tag(tag):
    scheme = tag_schema.load(tag, partial=True)
    if Tag.query.filter(
            Tag.name == tag_name).first() is None:
        tag = Tag(scheme.data.name, scheme.data.banned)
        db.session.add(tag)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, error="tag already exists")

@socketio.on('update tag')
@admin_only
def update_tag(tag):
    scheme = tag_schema.load(tag, partial=True)
    tag = Tag.query.get(scheme.data.id)
    if tag is not None:
        scheme = tag_schema.load(tag, partial=True)  
        tag.name = scheme.data.name
        tag.banned = scheme.data.banned
        db.session.add(tag)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, error="tag don't exists")

@socketio.on('delete tag')
@admin_only
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag is not None:
        db.session.delete(tag)
    db.session.commit()

#######
# GIF
#######

@socketio.on('get gif')
@admin_only
def gifs_from_blog(gif_id):
    gif = gif.query.get(gif_id)
    if gif is not None:
        return jsonify(success=True, gif=gif_schema.jsonify(gif))
    return jsonify(success=False, error="gif not found")

@socketio.on('random')
@authorized
def random_gif():
    return Gif.get_random_gif().url

@socketio.on('search gifs by tags')
@admin_only
def search_gifs(query):
    l_tags = query.split(' ')
    first = True
    gifs=[]
    for l_tag in l_tags:
        tag = Tag.query.filter(Tag.name==l_tag).first()
        if tag is not None:
            if first:
                first = False
                gifs = Gif.query.filter()
            else:
                gifs = set.intersection(gifs, Gif.query.filter())
                if gifs is []:
                    break
    return gifs_schema.jsonify(gifs)

@socketio.on('add gif')
@admin_only
def add_gif(gif):
    scheme = gif_schema.load(gif, partial=True)
    if Gif.query.filter(
            Gif.url == scheme.data.url).first() is None:
        gif = Gif(scheme.data.url, scheme.data.tags)
        db.session.add(gif)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, error="tag already exists")

@socketio.on('update gif')
@admin_only
def update_gif(gif):
    scheme = tag_schema.load(gif, partial=True)
    gif = Gif.query.get(scheme.data.id)
    if gif is not None:
        gif.tags = scheme.data.tags
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, error="gif doesn't exist")

@socketio.on('delete gif')
@admin_only
def delete_gif(gif_id):
    gif = Gif.query.get(gif_id)
    if gif is not None:
        db.session.delete(gif)
    db.session.commit()


###############
# ACHIEVEMENT
###############

@socketio.on('get achievements')
@admin_only
def get_achievements():
    return achievements_schema.jsonify(achievement.query.all())

@socketio.on('get achievement')
@admin_only
def get_achievement(achievement_id):
    achievement = Achievement.query.get(achievement_id)
    if achievement is not None:
        return jsonify(success=True, achievement=achievement_schema.jsonify(achievement))
    return jsonify(success=False, error="achievement not found")

@socketio.on('add achievement')
@admin_only
def add_achievement(achievement):
    scheme = achievement_schema.load(achievement, partial=True)
    if Achievement.query.filter(
            achievement.name == achievement_name).first() is None:
        achievement = Achievement(scheme.data.name,scheme.data.banned)
        achievement.title = scheme.data.title
        achievement.tags = scheme.data.tags
        achievement.condition = scheme.data.condition
        achievement.type_of = scheme.data.type_of
        achievement.icon = scheme.data.icon
        achievement.xp = scheme.data.xp
        db.session.add(achievement)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, error="achievement already exists")

@socketio.on('update achievement')
@admin_only
def update_achievement(achievement):
    scheme = achievement_schema.load(achievement, partial=True)
    achievement = Achievement.query.get(scheme.data.id)
    if achievement is not None:
        achievement.title = scheme.data.title
        achievement.tags = scheme.data.tags
        achievement.condition = scheme.data.condition
        achievement.type_of = scheme.data.type_of
        achievement.icon = scheme.data.icon
        achievement.xp = scheme.data.xp
        db.session.add(achievement)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, error="achievement doest not exist")

@socketio.on('delete achievement')
@admin_only
def delete_achievement(achievement_id):
    achievement = Achievement.query.get(achievement_id)
    if achievement is not None:
        db.session.delete(achievement)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, error="achievement doest not exist")

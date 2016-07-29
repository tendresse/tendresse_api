#! /usr/bin/env python

import os, yaml, urllib3, json, time
urllib3.disable_warnings() # disable unverified HTTPS warning

from flask_script import Manager

from app.models.gif import Gif
from app.models.success import Success
from app.models.tag import Tag

from app import create_app, db

app = create_app(os.getenv('APP_CONFIG', 'default'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = Manager(app)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def createdb():
    '''Creates db tables.'''
    db.create_all()

@manager.command
def dropdb():
    '''Creates db tables.'''
    db.drop_all()
    
@manager.command
def lowerusernames():
    '''lower all usernames'''
    from app.models.user import User
    users = User.query.all()
    for user in users:
        user.username = user.username.lower()
    db.session.commit()

@manager.command
def populatedb():
    '''Populate db with list of tumblrs in blogs.yml'''
    time_start_global = time.time()
    blogs = yaml.load(open("blogs.yml"))
    known_tags = {}
    avoided_tags = ["by","tumblr","star","famous","the","sexy","fucking","porn","gif","sex","sexe","xxx","scene","pr0n","fuck","huge","porno","gifs","pornstar","erotic","nsfw","naughty","horny","hot","a","an"]
    tumblr_key = 'Gm7u68GMu8RCQmIVV1vmr7QlToZ8rYKrzr1HsULlmK0doez73o'
    http = urllib3.PoolManager()
    for blog_url in blogs:
        time_start_blog = time.time()
        print("fetching : "+blog_url)
        blog_json_url = "https://api.tumblr.com/v2/blog/"+blog_url+"/posts/photo?api_key="+tumblr_key
        r = http.request('GET', blog_json_url)
        data = json.loads(r.data.decode('utf-8'))
        if data["meta"]["status"] is 200:
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
            time_end_blog = time.time()
            print("took : "+str(time_end_blog-time_start_blog)+" seconds for "+str(total_posts)+" gifs.")
        else:
            print("... tumblr is offline")
    time_end_global = time.time()
    print("populatedb took : "+str(time_end_global-time_start_global)+" seconds.")


@manager.command
def populategifsfromfile(filename):
    '''Populate db with gifs/tags from yaml file'''
    gifs = yaml.load(open(filename))
    avoided_tags = ["the","sexy","fucking","porn","gif","sex","sexe","xxx","scene","pr0n","fuck","huge","porno","gifs","pornstar","erotic","nsfw","naughty","horny","hot","a","an"]
    for gif in gifs:
        g = Gif(url=gif["url"])
        db.session.add(g)
        for tag in gif["tags"]:
            tag = tag.lower()
            if tag not in avoided_tags:
                t = Tag.query.get(tag)
                if t is None:
                    o = Tag(name=tag)
                    db.session.add(o)
                    db.session.commit()
                    g.tags.append(o)
                else:
                    g.tags.append(t)
        db.session.commit()
        
@manager.command
def populateachievementsfromfile(filename):
    '''Populate db with gifs/tags from yaml file'''
    achievements = yaml.load(open(filename))
    for achievement in achievements:
        s = Success(title=achievement["title"], type_of=achievement["type_of"], condition=achievement["condition"], icon=achievement["icon"])
        db.session.add(s)
        if achievement["type_of"] == "receive":
            for tag in achievement["tags"]:
                    t = Tag.query.filter(Tag.name==tag).first()
                    if t is None:
                        o = Tag(name=tag)
                        db.session.add(o)
                        db.session.commit()
                        t = o
                    s.tags.append(t)
    db.session.commit()
    
if __name__ == '__main__':
    manager.run()

#! /usr/bin/env python

import os, yaml, urllib3, json, codecs
from flask.ext.script import Manager

from app.models.gif import Gif
from app.models.success import Success
from app.models.tag import Tag

from app import create_app, db
from urllib.request import urlopen

app = create_app(os.getenv('APP_CONFIG', 'default'))
manager = Manager(app)
reader = codecs.getreader("utf-8")

@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def createdb():
    '''Creates db tables.'''
    db.create_all()

@manager.command
def populatedb():
    '''Populate db with list of tumblrs in '''
    # open the list of blogs
    blogs = yaml.load(open("blogs.yml"))
    tags = {}
    avoid_tags = ["porn","gif","sex","sexe","xxx","scene","pr0n","fuck","huge","porno","gifs"]
    tumblr_key = 'Gm7u68GMu8RCQmIVV1vmr7QlToZ8rYKrzr1HsULlmK0doez73o'
    # iterate through blogs
    for blog_url in blogs:
        # get the total_posts
        blog_json_url = "https://api.tumblr.com/v2/blog/"+blog_url+"/posts/photo?api_key="+tumblr_key
        response = urlopen(blog_json_url)
        data = json.load(reader(response))
        total_posts = data["response"]["total_posts"]
		# iterate from 0 to total_posts by 50
        blog_json_url+="&offset="
        for i in range(0,total_posts,50):
            # get the json
            response = urlopen(blog_json_url+str(i))
            data = json.load(reader(response))
            # iterate through json
            if data["meta"]["status"] is 200:
                for post in data["response"]["posts"]:
                    if post["type"] == "photo":
                        for photo in post["photos"]:
                            url_gif = photo["original_size"]["url"]
                            if url_gif[-3:] == "gif":
                                # photo["original_size"]["width"] pour trier si le gif est trop petit ?
                                post_tags = post["tags"]
                                # # add gif to db
                                gif = Gif(url=url_gif)
                                db.session.add(gif)
                                # # check if tag exists else add to db
                                for l_tag in post_tags:
                                    l_tag = l_tag.split(' ')
                                    for tag in l_tag:
                                        if tag not in avoid_tags:
                                            if tag != " " and tag !="" :
                                                if tag not in tags :
                                                    o = Tag(name=tag)
                                                    db.session.add(o)
                                                    db.session.commit()
                                                    tags[tag] = o
                                                # link tag to gif
                                                if tags[tag] not in gif.tags :
                                                    gif.tags.append(tags[tag])
                                db.session.commit()


if __name__ == '__main__':
    manager.run()

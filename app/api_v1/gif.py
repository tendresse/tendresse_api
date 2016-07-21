from flask import jsonify, request

from . import api
from .. import db
from ..models.gif import Gif, get_random_gif
from ..schemas.gif import gif_schema, gifs_schema


@api.route('/gifs', methods=['GET'])
def get_gifs():
    pass


@api.route('/random', methods=['GET'])
def get_random():
    return gif_schema.jsonify(get_random_gif()),200 

@api.route('/gifs/<int:id>', methods=['GET'])
def get_gif(id):
    return gif_schema.jsonify(Gif.query.get(id))


@api.route('/gifs', methods=['POST'])
def create_gif():
    pass


@api.route('/gifs/<int:id>', methods=['PUT'])
def update_gif(id):
    pass


@api.route('/gifs/<int:id>', methods=['DELETE'])
def delete_gif(id):
    Gif.query.get(id).delete()
    db.session.commit()
    return jsonify(state=True), 200

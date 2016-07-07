from flask import jsonify, request

from . import api
from .. import db
from ..models.gif import Gif
from ..schemas.gif import gif_schema, gifs_schema


@api.route('/gifs', methods=['GET'])
def get_gifs():
    pass


@api.route('/gifs/<int:id>', methods=['GET'])
def get_gif(id):
    pass


@api.route('/gifs', methods=['POST'])
def create_gif():
    pass


@api.route('/gifs/<int:id>', methods=['PUT'])
def update_gif(id):
    pass


@api.route('/gifs/<int:id>', methods=['DELETE'])
def delete_gif(id):
    pass

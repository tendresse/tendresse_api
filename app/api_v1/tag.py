from flask import jsonify, request

from . import api
from .. import db
from ..models.tag import Tag
from ..schemas.tag import tag_schema, tags_schema


@api.route('/tags', methods=['GET'])
def get_tags():
    pass


@api.route('/tags/<int:id>', methods=['GET'])
def get_tag(id):
    pass


@api.route('/tags', methods=['POST'])
def create_tag():
    pass


@api.route('/tags/<int:id>', methods=['PUT'])
def update_tag(id):
    pass


@api.route('/tags/<int:id>', methods=['DELETE'])
def delete_tag(id):
    pass

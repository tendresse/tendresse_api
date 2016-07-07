from flask import jsonify, request

from . import api
from .. import db
from ..models.success import Success
from ..schemas.success import success_schema, successes_schema


@api.route('/successes', methods=['GET'])
def get_successes():
    pass


@api.route('/successes/<int:id>', methods=['GET'])
def get_success(id):
    pass


@api.route('/successes', methods=['POST'])
def create_success():
    pass


@api.route('/successes/<int:id>', methods=['PUT'])
def update_success(id):
    pass


@api.route('/successes/<int:id>', methods=['DELETE'])
def delete_success(id):
    pass

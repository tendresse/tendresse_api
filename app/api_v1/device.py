from flask import jsonify, request

from . import api
from .. import db
from ..models.device import Device
from ..schemas.device import device_schema, devices_schema


@api.route('/devices', methods=['GET'])
def get_devices():
    pass


@api.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    pass


@api.route('/devices', methods=['POST'])
def create_device():
    pass


@api.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    pass


@api.route('/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    pass

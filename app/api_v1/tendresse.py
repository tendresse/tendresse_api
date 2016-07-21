from flask import jsonify, request

from . import api
from .. import db
from ..models.tendresse import Tendresse
from ..schemas.tendresse import tendresse_schema, tendresses_schema

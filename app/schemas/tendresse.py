from marshmallow import fields
from .. import ma
from ..models.tendresse import Tendresse
from ..schemas.user import user_schema, users_schema
from ..schemas.success import success_schema, successes_schema
from ..schemas.gif import gif_schema, gifs_schema


class TendresseSchema(ma.ModelSchema):

	id = fields.Int()
	sender = fields.Nested(user_schema, only=("username"))
	gif = fields.Nested(gif_schema, only=("url"))


tendresse_schema = TendresseSchema()
tendresses_schema = TendresseSchema(many=True)

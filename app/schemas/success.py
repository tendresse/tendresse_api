from .. import ma
from marshmallow import fields
from ..models.success import Success
from ..schemas.tag import tags_schema

class SuccessSchema(ma.ModelSchema):

	id = fields.Int()
	title = fields.String()
	tags = fields.Nested(tags_schema, only=("name"), many=True)
	condition = fields.Int()
	type_of = fields.String()
	icon = fields.String()

success_schema = SuccessSchema()
successes_schema = SuccessSchema(many=True)

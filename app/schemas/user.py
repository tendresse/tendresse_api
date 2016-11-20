from marshmallow import fields
from .. import ma
from ..models.user import User
from ..schemas.success import success_schema, successes_schema


class UserSchema(ma.ModelSchema):

	id = fields.Int()
	username = fields.String()
	achievements = fields.Nested(successes_schema, many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

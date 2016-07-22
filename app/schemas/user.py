from .. import ma
from ..models.user import User


class UserSchema(ma.ModelSchema):

    class Meta:
        fields = ("id", "username", "achievements")
        exclude = ("password", "friends", "devices")


user_schema = UserSchema()
users_schema = UserSchema(many=True)

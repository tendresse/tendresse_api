from .. import ma
from ..models.token import Token


class TokenSchema(ma.ModelSchema):

    class Meta:
        model = Token


token_schema = TokenSchema()
tokens_schema = TokenSchema(many=True)

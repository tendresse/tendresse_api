from marshmallow import fields
from .. import ma
from ..models.gif import Gif
from ..schemas.tag import tags_schema


class GifSchema(ma.ModelSchema):

	tags = fields.Nested(tags_schema, many=True)
    class Meta:
        model = Gif


gif_schema = GifSchema()
gifs_schema = GifSchema(many=True)

from .. import ma
from ..models.gif import Gif


class GifSchema(ma.ModelSchema):

    class Meta:
        model = Gif


gif_schema = GifSchema()
gifs_schema = GifSchema(many=True)

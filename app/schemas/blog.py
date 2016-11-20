from marshmallow import fields
from .. import ma
from ..models.blog import Blog
from ..schemas.gif import gifs_schema


class BlogSchema(ma.ModelSchema):

	gifs = fields.Nested(gifs_schema, many=True)
	class Meta:
        model = Blog


blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)
blogs_without_gifs_schema = BlogSchema(many=True, exclude=('gifs'))

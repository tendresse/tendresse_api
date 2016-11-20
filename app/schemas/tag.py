from marshmallow import fields
from .. import ma
from ..models.tag import Tag
from ..schemas.gif import gifs_schema
from ..schemas.achievement import achievements_without_tags_schema

class TagSchema(ma.ModelSchema):

	achievements = fields.Nested(achievements_without_tags_schema, many=True)
	gifs = fields.Nested(gifs_schema, only=("id","url"), many=True)
    class Meta:
        model = Tag


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
tags_without_gifs_schema = TagSchema(many=True, exclude=('gifs'))

from .. import ma
from ..models.tag import Tag


class TagSchema(ma.ModelSchema):

    class Meta:
        model = Tag


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

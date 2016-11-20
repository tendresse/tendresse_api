from .. import ma
from marshmallow import fields
from ..models.achievement import Achievement
from ..schemas.tag import tags_without_gifs_schema

class AchievementSchema(ma.ModelSchema):

	tags = fields.Nested(tags_without_gifs_schema, many=True)
	class Meta:
        model = Achievement

achievement_schema = AchievementSchema()
achievements_schema = AchievementSchema(many=True)
achievements_without_tags_schema = AchievementSchema(many=True, exclude=('tags'))
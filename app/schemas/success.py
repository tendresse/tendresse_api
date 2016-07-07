from .. import ma
from ..models.success import Success


class SuccessSchema(ma.ModelSchema):

    class Meta:
        model = Success


success_schema = SuccessSchema()
successes_schema = SuccessSchema(many=True)

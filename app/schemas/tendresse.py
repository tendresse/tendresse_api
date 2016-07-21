from .. import ma
from ..models.tendresse import Tendresse


class TendresseSchema(ma.ModelSchema):

    class Meta:
        model = Tendresse


tendresse_schema = TendresseSchema()
tendresses_schema = TendresseSchema(many=True)

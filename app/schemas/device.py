from .. import ma
from ..models.device import Device


class DeviceSchema(ma.ModelSchema):

    class Meta:
        model = Device


device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)

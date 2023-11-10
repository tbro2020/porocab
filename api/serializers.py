from rest_framework.serializers import ModelSerializer
from drf_extra_fields.geo_fields import PointField


def model_serializer_factory(model, fields='__all__', depth=1):
    cls_name = f"{model.__name__}Serializer"
    attrs = {
        "Meta": type("Meta", (), {"model": model, "fields": fields, "depth": depth})
    }
    return type(cls_name, (ModelSerializer,), attrs)
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import PrimaryKeyRelatedField
from django.contrib.gis.db import models
from drf_extra_fields import geo_fields

from core.models import User

def model_serializer_factory(model, fields='__all__', depth=1):
    cls_name = f"{model.__name__}Serializer"
    attrs = {field.name: geo_fields.PointField() 
             for field in model._meta.fields if isinstance(field, models.PointField)}
    attrs = {"Meta": type("Meta", (), {"model": model, "fields": fields, "depth": depth}), **attrs}
    return type(cls_name, (ModelSerializer,), attrs)
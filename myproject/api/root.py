from django.conf import settings
from django.db import models

from savory_pie.resources import APIResource
from savory_pie.django import fields
from savory_pie.django.resources import ModelResource, QuerySetResource

from myproject.models import Zone, Content, ZoneContent


class ZoneResource(ModelResource):
    fields = [
       fields.AttributeField('name', type=str),
       # fields.SubModelResourceField('owners', OwnerResource),
    ]
    model_class = Zone


class ZoneQuerySetResource(QuerySetResource):
    resource_path = 'zone'
    resource_class = ZoneResource
    page_size = 200


root_resource = APIResource()
root_resource.register_class(ZoneQuerySetResource)

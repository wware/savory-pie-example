#####################################
#                                   #
#         Savory Pie stuff          #
#                                   #
#####################################

from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from savory_pie.resources import APIResource
from savory_pie.django import fields, resources, filters

from myproject.models import Zone, Content, Segment, ZoneContent


class ZoneResource(resources.ModelResource):
    parent_resource_path = 'zone'
    model_class = Zone

    fields = [
        fields.AttributeField('name', type=str),
    ]


class ContentResource(resources.ModelResource):
    parent_resource_path = 'content'
    model_class = Content

    fields = [
        fields.AttributeField('title', type=str),
    ]


class SegmentResource(resources.ModelResource):
    parent_resource_path = 'segment'
    model_class = Segment

    fields = [
        fields.AttributeField('name', type=str),
    ]


class ZoneContentResource(resources.ModelResource):
    parent_resource_path = 'zonecontent'
    model_class = ZoneContent

    fields = [
        fields.SubModelResourceField('zone', ZoneResource),
        fields.SubModelResourceField('content', ContentResource),
        fields.SubModelResourceField('segment', SegmentResource)
    ]


class ZoneQuerySetResource(resources.QuerySetResource):
    resource_path = 'zone'
    resource_class = ZoneResource
    page_size = 200


class ContentQuerySetResource(resources.QuerySetResource):
    resource_path = 'content'
    resource_class = ContentResource
    page_size = 200


class SegmentQuerySetResource(resources.QuerySetResource):
    resource_path = 'segment'
    resource_class = SegmentResource
    page_size = 200


class ZoneContentQuerySetResource(resources.QuerySetResource):
    resource_path = 'zonecontent'
    resource_class = ZoneContentResource
    filters = [
        filters.StandardFilter('zoneOne', {'zone__id': 1}),
        filters.ParameterizedFilter('zone', 'zone__id'),
    ]

root_resource = APIResource()
root_resource.register_class(ZoneQuerySetResource)
root_resource.register_class(ContentQuerySetResource)
root_resource.register_class(ZoneContentQuerySetResource)

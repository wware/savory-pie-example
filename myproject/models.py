import logging

from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from savory_pie.django import fields, resources, filters

logger = logging.getLogger(__name__)


####### Here's how inlines work in the admin page ##########


class Person(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return "<%s>" % self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')
    def __str__(self):
        return "<%s>" % self.name

class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)

class GroupAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)

admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Membership)


#######


class Zone(models.Model):
    """
    A Zone is a content place holder.

    """
    name = models.CharField(_('Name'), max_length=100)

    def to_json(self):
        return {"type": self.__class__.__name__, "name": self.name}

    def __str__(self):
        return "<Zone: %s>" % self.name


class Content(models.Model):
    """
    The Content model holds markdown that will be displayed in a zone.

    """
    title = models.CharField(_(u'Title'), max_length=255, blank=False)
    zones = models.ManyToManyField(Zone, through='ZoneContent')

    def to_json(self):
        return {"type": self.__class__.__name__, "title": self.title}

    def __str__(self):
        return "<Content: %s>" % self.title


class Segment(models.Model):
    """
    Some documentation about Segment.

    """
    name = models.CharField(_('Name'), max_length=100)

    def to_json(self):
        return {"type": self.__class__.__name__, "name": self.name}

    def __str__(self):
        return "<Segment: %s>" % self.name


class ZoneContent(models.Model):
    """
    The ZoneContent model is used to relate a Zone to a specific Content object.

    """
    zone = models.ForeignKey(Zone)
    content = models.ForeignKey(Content)
    segment = models.ForeignKey(Segment)

    def to_json(self):
        return {"type": self.__class__.__name__, "zone": self.zone, "content": self.content, "segment": self.segment}

    def __str__(self):
        return "<ZoneContent: %s ; %s ; %s>" % (repr(self.zone), repr(self.content), repr(self.segment))


class ZoneAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)


class ZoneContentAdmin(admin.ModelAdmin):
    list_display = ("id", "zone", "content", "segment",)
    list_filter = ("zone__name",)


class SegmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(ZoneContent, ZoneContentAdmin)

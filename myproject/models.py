import logging

from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


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


class ZoneContent(models.Model):
    """
    The ZoneContent model is used to relate a Zone to a specific Content object.

    """
    zone = models.ForeignKey(Zone)
    content = models.ForeignKey(Content)

    def to_json(self):
        return {"type": self.__class__.__name__, "zone": self.zone, "content": self.content}

    def __str__(self):
        return "<ZoneContent: %s ; %s>" % (repr(self.zone), repr(self.content))


if False:
    admin.site.register(Zone)
    admin.site.register(Content)
    admin.site.register(ZoneContent)
else:
    class ZoneAdmin(admin.ModelAdmin):
        list_display = ("id", "name",)
    admin.site.register(Zone, ZoneAdmin)

    class ContentAdmin(admin.ModelAdmin):
        list_display = ("id", "title",)
    admin.site.register(Content, ContentAdmin)

    class ZoneContentAdmin(admin.ModelAdmin):
        list_display = ("id", "zone", "content",)
        list_filter = ("zone__name",)
    admin.site.register(ZoneContent, ZoneContentAdmin)

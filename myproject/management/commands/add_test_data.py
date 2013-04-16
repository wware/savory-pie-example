from django.core.management.base import BaseCommand

from myproject import models


class Command(BaseCommand):

    help = 'Create some data for testing.'

    def handle(self, **options):

        z1 = models.Zone()
        z1.name = "abcd"
        z1.save()
        z2 = models.Zone()
        z2.name = "efgh"
        z2.save()
        c1 = models.Content()
        c1.title = "A Tree Grows in Brooklyn"
        c1.save()
        c2 = models.Content()
        c2.title = "The Sun Also Rises"
        c2.save()
        s1 = models.Segment()
        s1.name = "stuv"
        s1.save()
        s2 = models.Segment()
        s2.name = "wxyz"
        s2.save()
        z = models.ZoneContent()
        z.zone = z1
        z.content = c1
        z.segment = s1
        z.save()
        z = models.ZoneContent()
        z.zone = z2
        z.content = c2
        z.segment = s2
        z.save()

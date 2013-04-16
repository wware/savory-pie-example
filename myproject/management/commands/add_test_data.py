from django.core.management.base import BaseCommand

from myproject import models


class Command(BaseCommand):

    help = 'Create some data for testing.'

    def handle(self, **options):
        z1 = models.Zone(name='abcd'); z1.save()
        z2 = models.Zone(name='efgh'); z2.save()
        c1 = models.Content(title='A Tree Grows in Brooklyn'); c1.save()
        c2 = models.Content(title='The Sun Also Rises'); c2.save()
        s1 = models.Segment(name='stuv'); s1.save()
        s2 = models.Segment(name='wxyz'); s2.save()
        models.ZoneContent(zone=z1, content=c1, segment=s1).save()
        models.ZoneContent(zone=z2, content=c2, segment=s2).save()

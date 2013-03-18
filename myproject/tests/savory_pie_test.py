from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.unittest import skip
from django.utils.unittest.case import skipIf

from myproject import models

import json

DEBUG = True


class DumbTest(TestCase):

    def setUp(self):
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

    def fetch(self, url):
        resp = self.client.get(url)
        content = json.loads(resp.content)
        if DEBUG:
            if content.has_key('error'):
                import sys
                sys.stderr.write(content['error'])
        return content

    def test_basic(self):
        content = self.fetch('/api/zonecontent')
        meta = content['meta']
        self.assertEqual(2, meta['count'])
        zc = content['objects'][0]
        self.assertTrue('/api/zonecontent/' in zc['resourceUri'])
        self.assertEqual('A Tree Grows in Brooklyn', zc['content']['title'])
        self.assertEqual('abcd', zc['zone']['name'])
        self.assertEqual('stuv', zc['segment']['name'])
        zc = content['objects'][1]
        self.assertTrue('/api/zonecontent/' in zc['resourceUri'])
        self.assertEqual('The Sun Also Rises', zc['content']['title'])
        self.assertEqual('efgh', zc['zone']['name'])
        self.assertEqual('wxyz', zc['segment']['name'])

    def test_standard_filter(self):
        content = self.fetch('/api/zonecontent?zone_1=')
        meta = content['meta']
        self.assertEqual(1, meta['count'])
        zc = content['objects'][0]
        self.assertTrue('/api/zonecontent/' in zc['resourceUri'])
        self.assertEqual('A Tree Grows in Brooklyn', zc['content']['title'])
        self.assertEqual('abcd', zc['zone']['name'])
        self.assertEqual('stuv', zc['segment']['name'])

    def test_parameterized_filter(self):
        content = self.fetch('/api/zonecontent?zone=1')
        meta = content['meta']
        self.assertEqual(1, meta['count'])
        zc = content['objects'][0]
        self.assertTrue('/api/zonecontent/' in zc['resourceUri'])
        self.assertEqual('A Tree Grows in Brooklyn', zc['content']['title'])
        self.assertEqual('abcd', zc['zone']['name'])
        self.assertEqual('stuv', zc['segment']['name'])
        #
        content = self.fetch('/api/zonecontent?zone=2')
        meta = content['meta']
        self.assertEqual(1, meta['count'])
        zc = content['objects'][0]
        self.assertTrue('/api/zonecontent/' in zc['resourceUri'])
        self.assertEqual('The Sun Also Rises', zc['content']['title'])
        self.assertEqual('efgh', zc['zone']['name'])
        self.assertEqual('wxyz', zc['segment']['name'])

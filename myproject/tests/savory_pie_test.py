from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.unittest import skip
from django.utils.unittest.case import skipIf
from django.core.management import call_command

from myproject import models

import json

DEBUG = True


class DumbTest(TestCase):

    def setUp(self):
        call_command('add_test_data')

    def tearDown(self):
        models.Zone.objects.all().delete()
        models.Content.objects.all().delete()
        models.Segment.objects.all().delete()
        models.ZoneContent.objects.all().delete()

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
        content = self.fetch('/api/zonecontent?zoneOne=')
        # import sys, pprint; print >> sys.stderr; pprint.pprint(content, stream=sys.stderr)
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

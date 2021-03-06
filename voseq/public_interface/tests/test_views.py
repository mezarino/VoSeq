import json
import os

from django.core.management import call_command
from django.test import Client
from django.test import TestCase
from django.test.utils import override_settings
import haystack

from public_interface.models import Vouchers
from public_interface.models import FlickrImages
from public_interface.models import Sequences


# Need to use a clean index for our tests
TEST_INDEX = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'TIMEOUT': 60 * 10,
        'INDEX_NAME': 'test_index',
    },
}


@override_settings(HAYSTACK_CONNECTIONS=TEST_INDEX)
class TestViews(TestCase):
    def setUp(self):
        args = []
        opts = {'dumpfile': 'test_db_dump.xml', 'verbosity': 0}
        cmd = 'migrate_db'
        call_command(cmd, *args, **opts)

        # build index with our test data
        haystack.connections.reload('default')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super(TestViews, self).setUp()

        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_browse(self):
        response = self.client.get('/browse/')
        self.assertEqual(200, response.status_code)

    def test_show_voucher(self):
        response = self.client.get('/p/CP100-10', follow=True)
        self.assertEqual(200, response.status_code)

    def test_show_voucher_doesnt_exist(self):
        response = self.client.get('/p/NN1-1aaaaaaa', follow=True)
        self.assertEqual(404, response.status_code)

    def test_show_sequence(self):
        response = self.client.get('/s/CP100-10/COI/')
        self.assertEqual(200, response.status_code)

    def test_show_sequence_doesnt_exist(self):
        response = self.client.get('/s/NN1-1aaaaa/EF1a/')
        self.assertEqual(404, response.status_code)

    def test_search_hymenoptera(self):
        response = self.client.get('/search/?orden=Hymenoptera')
        content = str(response.content)
        self.assertTrue('CP100-14' in content)

    def test_search_returns_empty(self):
        """
        Querying for several data fields should be equivalent of using AND."
        """
        response = self.client.get('/search/?orden=Coleoptera&code=NN1-1')
        content = str(response.content)
        self.assertFalse('NN1-2' in content and 'NN1-1' in content)

    def test_advanced_search(self):
        response = self.client.get('/search/')
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        call_command('clear_index', interactive=False, verbosity=0)

import os
import unittest2 as unittest
from resty import Client, LazyJsonDocument, Service, Collection, Resource


def disk_loader(uri):
    fixture_dir = os.path.join(os.path.dirname(__file__), 'mocks')
    fixture_path = os.path.join(fixture_dir, uri)
    mime_type = 'application/json'
    content = open(fixture_path).read()
    return (mime_type, content)


client = Client(disk_loader)
client.register_document_parser('application/json', LazyJsonDocument)
client.register_document('application/vnd.test-service+json', Service)
client.register_document(
    'application/vnd.test-collection+json', Collection
)
client.register_document('application/vnd.test-resource+json', Resource)


class TestClient(unittest.TestCase):

    def _get_target(self):
        return client

    def test_available_services(self):
        c = self._get_target()
        home = c.load('entrypoint.json')
        car_collection = home.service('cars')
        self.assertEqual(len(car_collection.items()), 3)
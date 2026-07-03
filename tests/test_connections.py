from django.core.mail import backends
from django.test import TestCase

from .test_backends import ErrorRaisingBackend
from post_office.connections import connections


class ConnectionTest(TestCase):
    def test_get_connection(self):
        # Ensure ConnectionHandler returns the right connection
        self.assertTrue(isinstance(connections.get('error'), ErrorRaisingBackend))
        self.assertTrue(isinstance(connections.get('locmem'), backends.locmem.EmailBackend))

    def test_close_evicts_cache(self):
        # Ensure connections.close() clears the cache so the next get()
        # yields a freshly-opened connection. Without this, backends that null
        # out their client on close() (e.g. Amazon SES) would hand out dead
        # connections on subsequent batches.
        first = connections.get('locmem')
        connections.close()
        second = connections.get('locmem')
        self.assertIsNot(first, second)

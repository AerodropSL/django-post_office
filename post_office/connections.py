from threading import local

from django.core.mail import get_connection

from .settings import get_backend


# Copied from Django 1.8's django.core.cache.CacheHandler
class ConnectionHandler:
    """
    A Cache Handler to manage access to Cache instances.

    Ensures only one instance of each alias exists per thread.
    """

    def __init__(self):
        self._connections = local()

    def get(self, alias, key=None, **kwargs):
        if key is None:
            key = alias

        try:
            return self._connections.connections[key]
        except AttributeError:
            self._connections.connections = {}
        except KeyError:
            pass

        try:
            backend = get_backend(alias)
        except KeyError:
            raise KeyError('%s is not a valid backend alias' % alias)

        connection = get_connection(backend, **kwargs)
        connection.open()
        self._connections.connections[key] = connection
        return connection

    def all(self):
        return getattr(self._connections, 'connections', {}).values()

    def close(self):
        for connection in self.all():
            connection.close()
        # We need to clean up connections, so they are recreated as config might have changed
        if hasattr(self._connections, 'connections'):
            self._connections.connections = {}


connections = ConnectionHandler()

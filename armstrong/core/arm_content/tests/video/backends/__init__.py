from fudge.inspector import arg
from ..._utils import *

from .youtube import *
from .vimeo import *

from ....video import backends
from armstrong.utils.backends.base import MultipleBackendProxy
from armstrong.utils.backends import base


class TestableBackend(object):
    pass


class SomeOtherTestableBackend(object):
    pass


class GetBackendTestCase(TestCase):
    def backend_name(self, name):
        return "%s.%s" % (self.__module__, name)

    def test_uses_backend_from_settings(self):
        backend_name = self.backend_name('TestableBackend')
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=backend_name)

        backends.backend.settings = settings
        backend = backends.get_backend()
        self.assertIsA(backend, TestableBackend)

    def test_uses_injected_settings_if_provided(self):
        backend_name = self.backend_name('SomeOtherTestableBackend')
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=backend_name)
        backends.backend.settings = settings

        backend = backends.get_backend()
        self.assertIsA(backend, SomeOtherTestableBackend)

    def test_returns_MultipleBackend_if_configured_with_a_list(self):
        my_backends = [self.backend_name('TestableBackend'),
                self.backend_name('SomeOtherTestableBackend')]

        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=my_backends)
        backends.backend.settings = settings

        backend = backends.get_backend()
        self.assertIsA(backend, MultipleBackendProxy)

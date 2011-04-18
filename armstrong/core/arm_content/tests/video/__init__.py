from .._utils import *

from ...video import backends


class TestableBackend(object):
    pass


class SomeOtherTestableBackend(object):
    pass


class GetBackendTestCase(TestCase):
    def test_uses_backend_from_settings(self):
        backend_name = "%s.TestableBackend" % self.__module__
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=backend_name)

        with fudge.patched_context(backends, 'default_settings', settings):
            backend = backends.get_backend()
            self.assertEqual(backend, TestableBackend)

    def test_uses_injected_settings_if_provided(self):
        backend_name = "%s.SomeOtherTestableBackend" % self.__module__
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=backend_name)

        fudge.clear_calls()

        backend = backends.get_backend(settings=settings)
        self.assertEqual(backend, SomeOtherTestableBackend)

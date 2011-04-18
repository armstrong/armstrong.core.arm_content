from .._utils import *

from ...video import backends


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

        with fudge.patched_context(backends, 'default_settings', settings):
            backend = backends.get_backend()
            self.assertEqual(backend, TestableBackend)

    def test_uses_injected_settings_if_provided(self):
        backend_name = self.backend_name('SomeOtherTestableBackend')
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=backend_name)

        fudge.clear_calls()

        backend = backends.get_backend(settings=settings)
        self.assertEqual(backend, SomeOtherTestableBackend)

    def test_returns_MultipleBackend_if_configured_with_a_list(self):
        my_backends = [self.backend_name('TestableBackend'),
                self.backend_name('SomeOtherTestableBackend')]

        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=my_backends)

        backend = backends.get_backend(settings=settings)
        self.assertEqual(backend, backends.MultipleBackends)


class MultipleBackendsTestCase(TestCase):
    def test_each_backend_is_called_until_one_answers_with_non_none(self):
        expected = ("foo", "bar", random.randint(100, 200))
        one = fudge.Fake()
        one.expects('parse').with_args('foo/bar').returns(None)

        two = fudge.Fake()
        two.expects('parse').with_args('foo/bar').returns(expected)

        fudge.clear_calls()

        backend = backends.MultipleBackends(one, two)
        self.assertEqual(expected, backend.parse('foo/bar'))

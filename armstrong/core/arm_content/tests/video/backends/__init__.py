from fudge.inspector import arg
from ..._utils import *

from .youtube import *
from .vimeo import *

from ....video import backends


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
            self.assertIsA(backend, TestableBackend)

    def test_uses_injected_settings_if_provided(self):
        backend_name = self.backend_name('SomeOtherTestableBackend')
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=backend_name)

        fudge.clear_calls()

        backend = backends.get_backend(settings=settings)
        self.assertIsA(backend, SomeOtherTestableBackend)

    def test_returns_MultipleBackend_if_configured_with_a_list(self):
        my_backends = [self.backend_name('TestableBackend'),
                self.backend_name('SomeOtherTestableBackend')]

        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=my_backends)

        backend = backends.get_backend(settings=settings)
        self.assertIsA(backend, backends.MultipleBackends)

    def test_MultipleBackend_is_passed_configured_objects(self):

        def is_TestableBackend(obj):
            return isinstance(obj, TestableBackend)

        def is_SomeOtherTestableBackend(obj):
            return isinstance(obj, SomeOtherTestableBackend)

        fake = fudge.Fake(backends.MultipleBackends)
        fake.expects('__init__').with_args(arg.passes_test(is_TestableBackend),
                arg.passes_test(is_SomeOtherTestableBackend))

        my_backends = [self.backend_name('TestableBackend'),
                self.backend_name('SomeOtherTestableBackend')]
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=my_backends)

        with fudge.patched_context(backends, 'MultipleBackends', fake):
            backends.get_backend(settings=settings)


class NeverMatchesBackend(object):
    def prepare(self, video):
        return None


class AlwayMatchesBackend(object):
    def prepare(self, video):
        video.url, video.id = video.raw_url.split("?")
        return True


class MultipleBackendsTestCase(TestCase):
    def test_each_backend_is_called_until_one_answers_with_non_none(self):
        backend = backends.MultipleBackends(NeverMatchesBackend(),
                AlwayMatchesBackend())
        video = EmbeddedVideo(backend=backend)

        first = "first-%d" % random.randint(100, 200)
        second = "second-%d" % random.randint(100, 200)
        video.raw_url = "%s?%s" % (first, second)

        self.assertTrue(backend.prepare(video))
        self.assertEqual(first, video.url)
        self.assertEqual(second, video.id)

    def test_returns_not_True_if_no_backends_match(self):
        backend = backends.MultipleBackends(NeverMatchesBackend())
        video = EmbeddedVideo(backend=backend)
        video.raw_url = "some-random-url"

        self.assertFalse(backend.prepare(video))

    def test_sets_backend_on_EmbeddedVideo_to_the_backend_that_was_found(self):
        backend = backends.MultipleBackends(NeverMatchesBackend(),
                AlwayMatchesBackend())
        video = EmbeddedVideo(backend=backend)

        first = "first-%d" % random.randint(100, 200)
        second = "second-%d" % random.randint(100, 200)
        video.raw_url = "%s?%s" % (first, second)

        backend.prepare(video)
        self.assertIsA(video.backend, AlwayMatchesBackend)

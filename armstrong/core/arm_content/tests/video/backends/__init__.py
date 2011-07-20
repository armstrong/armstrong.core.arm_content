import fudge
from fudge.inspector import arg
import random
from ..._utils import *

from .youtube import *
from .vimeo import *

from ....video import backends
from ....video.backends import helpers
from armstrong.utils.backends.base import MultipleBackendProxy
from armstrong.utils.backends import base


class TestableBackend(object):
    pass


class SomeOtherTestableBackend(object):
    pass


class GetBackendTestCase(ArmContentTestCase):
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


class InjectDefaultsDecoratorTestCase(ArmContentTestCase):
    def test_provides_default_width_and_height(self):
        random_width = random.randint(1000, 2000)
        random_height = random.randint(1000, 2000)
        embed = object()
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EMBED_VIDEO_WIDTH=random_width,
                ARMSTRONG_EMBED_VIDEO_HEIGHT=random_height)
        fake = fudge.Fake()
        fake.is_callable().with_args(self, embed, random_width, random_height)

        with fudge.patched_context(helpers, "settings", settings):
            foo = helpers.inject_defaults(fake)
            foo(self, embed)

    def test_kwargs_are_passed_through_to_backend(self):
        random_kwargs = dict(
                [("key_%d" % i, i) for i in range(random.randint(10, 20))])
        random_width = random.randint(1000, 2000)
        random_height = random.randint(1000, 2000)
        embed = object()
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EMBED_VIDEO_WIDTH=random_width,
                ARMSTRONG_EMBED_VIDEO_HEIGHT=random_height)
        fake = fudge.Fake()
        fake.is_callable().with_args(self, embed, random_width, random_height,
                **random_kwargs)

        with fudge.patched_context(helpers, "settings", settings):
            foo = helpers.inject_defaults(fake)
            foo(self, embed, **random_kwargs)

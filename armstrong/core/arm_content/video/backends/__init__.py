import pkg_resources
pkg_resources.declare_namespace(__name__)

from django.conf import settings as default_settings
from django.utils.importlib import import_module

from .youtube import YouTubeBackend
from .vimeo import VimeoBackend


class MultipleBackends(object):
    def __init__(self, *others):
        self.others = others

    def prepare(self, video):
        for other in self.others:
            if other.prepare(video) is not None:
                video.backend = other
                return True


def get_backend(settings=None):
    if not settings:
        settings = default_settings

    backend_name = settings.ARMSTRONG_EXTERNAL_VIDEO_BACKEND

    def to_backend(a):
        module, backend_class = a.rsplit(".", 1)
        backend_module = import_module(module)
        return getattr(backend_module, backend_class)()

    if type(backend_name) is str:
        # TODO: Should raise an ImproperlyConfigured error if this isn't
        #       present in the settings variable.
        return to_backend(settings.ARMSTRONG_EXTERNAL_VIDEO_BACKEND)
    else:
        return MultipleBackends(*[to_backend(a) for a in
            settings.ARMSTRONG_EXTERNAL_VIDEO_BACKEND])

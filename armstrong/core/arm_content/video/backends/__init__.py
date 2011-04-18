import pkg_resources
pkg_resources.declare_namespace(__name__)

from django.conf import settings as default_settings
from django.utils.importlib import import_module

from .youtube import YouTubeBackend


class MultipleBackends(object):
    def __init__(self, *others):
        self.others = others

    def parse(self, url):
        for other in self.others:
            result = other.parse(url)
            if result is not None:
                return result


def get_backend(settings=None):
    if not settings:
        settings = default_settings

    backend_name = settings.ARMSTRONG_EXTERNAL_VIDEO_BACKEND
    if type(backend_name) is str:
        # TODO: Should raise an ImproperlyConfigured error if this isn't
        #       present in the settings variable.
        module, backend_class = settings.ARMSTRONG_EXTERNAL_VIDEO_BACKEND.rsplit(".", 1)
        backend_module = import_module(module)
        return getattr(backend_module, backend_class)
    else:
        return MultipleBackends

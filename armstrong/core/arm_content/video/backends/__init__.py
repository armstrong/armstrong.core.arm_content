import pkg_resources
pkg_resources.declare_namespace(__name__)

from django.conf import settings
from django.utils.importlib import import_module

from .youtube import YouTubeBackend


def get_backend():
    # TODO: Should raise an ImproperlyConfigured error if this isn't
    #       present in the settings variable.
    module, backend_class = settings.ARMSTRONG_EXTERNAL_VIDEO_BACKEND.rsplit(".", 1)
    backend_module = import_module(module)
    return getattr(backend_module, backend_class)

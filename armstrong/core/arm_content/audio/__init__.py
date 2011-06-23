
import pkg_resources
pkg_resources.declare_namespace(__name__)

from django.conf import settings as default_settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

def get_backend(settings=None,setting_name='ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND'):
    if not settings:
        settings = default_settings
    try:
        backend_name = getattr(settings, setting_name)
    except AttributeError:
        raise ImproperlyConfigured

    def to_backend(a):
        module, backend_class = a.rsplit(".", 1)
        backend_module = import_module(module)
        return getattr(backend_module, backend_class)()
    
    return to_backend(settings.ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND)

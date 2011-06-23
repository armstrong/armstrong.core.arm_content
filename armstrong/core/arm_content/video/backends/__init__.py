import pkg_resources
pkg_resources.declare_namespace(__name__)

from armstrong.utils.backends import GenericBackend
from django.conf import settings as default_settings
from django.utils.importlib import import_module

from .youtube import YouTubeBackend
from .vimeo import VimeoBackend


backend = GenericBackend("ARMSTRONG_EXTERNAL_VIDEO_BACKEND")
get_backend = backend.get_backend

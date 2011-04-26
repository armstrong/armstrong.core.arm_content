import pkg_resources
pkg_resources.declare_namespace(__name__)

from .authors import AuthorsMixin
from .video import EmbeddedVideoMixin

import pkg_resources
pkg_resources.declare_namespace(__name__)

from .authors import AuthorsMixin
from .images import *
from .publication import PublicationMixin
from .video import EmbeddedVideoMixin

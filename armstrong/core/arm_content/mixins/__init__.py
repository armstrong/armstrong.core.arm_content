import pkg_resources
pkg_resources.declare_namespace(__name__)

from .authors import AuthorsMixin
from .video import EmbeddedVideoMixin

# TODO: move this into the correct location
from ..publication.models import PublicationMixin

from .base import BaseImageMixin
from .sorl import SorlImageMixin

try:
    from .sorl import SorlImageMixin
except ImportError:
    pass

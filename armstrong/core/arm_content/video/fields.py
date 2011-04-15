from django.conf import settings
from django.db import models
from django.utils.importlib import import_module


class EmbeddedVideo(object):
    def __init__(self, url=None, backend=None):
        if not backend:
            # TODO: Should raise an ImproperlyConfigured error if this isn't
            #       present in the settings variable.
            module, backend_class = settings.ARMSTRONG_EXTERNAL_VIDEO_BACKEND.rsplit(".", 1)
            backend_module = import_module(module)
            backend = getattr(backend_module, backend_class)
        self.backend = backend()
        self.raw_url = url
        self.id = None
        if url:
            (self.url, self.id) = self.backend.parse(url)

    @property
    def type(self):
        return self.backend.type


class EmbeddedVideoField(models.URLField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(EmbeddedVideoField, self).__init__(self, *args, **kwargs)

    def get_prep_value(self, value):
        return value.raw_url

    def to_python(self, value):
        if isinstance(value, EmbeddedVideo):
            return value

        return EmbeddedVideo(value)

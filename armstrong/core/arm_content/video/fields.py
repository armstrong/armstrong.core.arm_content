from django.db import models

from .backends import get_backend


class EmbeddedVideo(object):
    def __init__(self, url=None, backend=None):
        if not backend:
            backend = get_backend()
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

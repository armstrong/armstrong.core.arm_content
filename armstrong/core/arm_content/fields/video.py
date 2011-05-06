from django.db import models

from ..video.backends import get_backend


class EmbeddedVideo(object):
    def __init__(self, url=None, backend=None):
        if not backend:
            backend = get_backend()
        self.backend = backend
        self.raw_url = url
        self.id = None
        if url:
            self.backend.prepare(self)

    @property
    def type(self):
        return self.backend.type

    def embed(self, **kwargs):
        return self.backend.embed(self, **kwargs)


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

    def formfield(self, **kwargs):
        defaults = {
            "label": "Embedded Video URL",
        }
        defaults.update(**kwargs)
        return super(EmbeddedVideoField, self).formfield(**defaults)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "%s.%s" % (self.__class__.__module__,
                self.__class__.__name__)
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

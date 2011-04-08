from django.conf import settings
from django.db import models
from django.utils.importlib import import_module
import urllib2


class YouTubeBackend(object):
    type = "YouTube"

    def parse(self, value):
        url = urllib2.urlparse.urlparse(value)
        query = urllib2.urlparse.parse_qs(url.query)['v'][0]
        return (url, query)


class ExternalVideo(object):
    def __init__(self, url=None, backend=None):
        if not backend:
            # TODO: Should raise an ImproperlyConfigured error if this isn't
            #       present in the settings variable.
            module, backend_class = settings.ARMSTRONG_EXTERNAL_VIDEO_BACKEND.rsplit(".", 1)
            backend_module = import_module(module)
            backend = getattr(backend_module, backend_class)
        self.backend = backend()
        self.raw_url = url
        self.query = None
        if url:
            (self.url, self.query) = self.backend.parse(url)

    @property
    def id(self):
        return self.query

    @property
    def type(self):
        return self.backend.type


class VideoField(models.URLField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(VideoField, self).__init__(self, *args, **kwargs)

    def get_prep_value(self, value):
        return value.raw_url

    def to_python(self, value):
        if isinstance(value, ExternalVideo):
            return value

        return ExternalVideo(value)

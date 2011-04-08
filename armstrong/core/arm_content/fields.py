from django.db import models
from django.db.models.fields.subclassing import Creator
import urllib2


def extract_id(self):
    return self.source.id
extract_id = property(extract_id)


def extract_type(self):
    return self.source.type
extract_type = property(extract_type)


class ExternalVideo(object):
    def __init__(self, url):
        self.raw_url = url
        self.query = False
        if url:
            self.url = urllib2.urlparse.urlparse(url)
            self.query = urllib2.urlparse.parse_qs(self.url.query)

    @property
    def id(self):
        if self.query:
            return self.query['v'][0]
        return None

    @property
    def type(self):
        return "YouTube"


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

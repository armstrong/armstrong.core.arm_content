from __future__ import absolute_import
from django.conf import settings
from django.db import models
from ..mixins.authors import AuthorsMixin

try:
    from sorl.thumbnail import ImageField
except ImportError:
    from django.db.models import ImageField

UPLOAD_PATH = getattr(settings, 'ARMSTRONG_IMAGES_UPLOAD_PATH',
    'armstrong/images/')

class ImageBase(AuthorsMixin):
    '''Abstract base class for image item'''
    image = ImageField(upload_to=UPLOAD_PATH)
    title = models.CharField(max_length=100)
    caption = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.image.url

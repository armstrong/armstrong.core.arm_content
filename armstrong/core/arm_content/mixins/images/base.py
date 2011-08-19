from __future__ import absolute_import
from django.db import models
from django.conf import settings

try:
    from sorl.thumbnail import ImageField
except ImportError:
    from django.db.models import ImageField

class BaseThumbnailMixin(object):
    '''Properties of an image-centric content item.'''
    visual_type = 'image'
    is_visual_embedded = False

    def render_visual(self, preset_label, presets=None, defaults=None, *args, **kwargs):
        raise NotImplementedError()

    def get_visual_thumbnail_url(self, preset_label, presets=None, defaults=None, *args, **kwargs):
        raise NotImplementedError()

UPLOAD_PATH = getattr(settings, 'ARMSTRONG_IMAGES_UPLOAD_PATH',
    'armstrong/images/')

class ImageMixin(models.Model):
    ''' Abstract mixin for images '''
    image = ImageField(upload_to=UPLOAD_PATH)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return self.image.url

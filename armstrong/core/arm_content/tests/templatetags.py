from ._utils import *
import datetime
from django.db import models
from django import template
from taggit.managers import TaggableManager

from .arm_content_support.models import SorlImage

from armstrong.core.arm_content.templatetags import content_helpers


class ThumbnailTestCase(ArmContentTestCase):
    def test_thumbnail_filter(self):
        thumb_url = "http://example.com/thumbnail_url.jpg"
        obj = { 'image': "image"}
        t = template.Template("{% load content_helpers %}{{ obj.image|thumbnail:'thumb_size' }}")

        thumbnail_result = fudge.Fake()
        thumbnail_result.has_attr(url=thumb_url)

        get_preset_thumbnail = fudge.Fake()
        get_preset_thumbnail.expects_call().\
                with_args("image", u'thumb_size').\
                returns(thumbnail_result)
        with fudge.patcher.patched_context(content_helpers, 
                    'get_preset_thumbnail',
                    get_preset_thumbnail):
            result = t.render(template.Context({'obj': obj}))
        self.assertEqual(result, thumb_url)
        fudge.verify()

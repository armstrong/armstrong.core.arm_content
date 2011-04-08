from django.db import models
from ._utils import *
from .arm_content_support.models import SimpleVideoModel

from ..fields import ExternalVideo


class VideoFieldTestCase(TestCase):
    def test_models_with_a_VideoField_have_a_source_type(self):
        video = SimpleVideoModel()
        self.assertTrue(hasattr(video, 'source_type'))

    def test_models_with_a_VideoField_have_a_source_id(self):
        video = SimpleVideoModel()
        self.assertTrue(hasattr(video, "source_id"))

    def test_settings_a_source_to_a_YouTube_url_stores_the_source_id(self):
        random_id = "abcdef%d" % random.randint(100, 200)
        video = SimpleVideoModel()
        video.source = "http://www.youtube.com/watch?v=%s" % random_id
        self.assertEqual(random_id, video.source_id)

    def test_videos_on_YouTube_have_a_source_type_of_YouTube(self):
        random_id = "abcdef%d" % random.randint(100, 200)
        video = SimpleVideoModel()
        video.source = "http://www.youtube.com/watch?v=%s" % random_id
        self.assertEqual("YouTube", video.source_type)

    def test_can_take_an_ExternalVideo_object_as_a_type(self):
        v = ExternalVideo("http://www.youtube.com/watch?v=abc")
        video = SimpleVideoModel()
        video.source = v
        self.assertEqual("YouTube", video.source_type, msg="sanity check")
        self.assertEqual("abc", video.source_id, msg="sanity check")

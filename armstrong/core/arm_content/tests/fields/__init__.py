from django.db import models
import fudge

from .._utils import *
from ..arm_content_support.models import SimpleVideoModel

from ...video import EmbeddedVideo
from ...video import fields


class ExampleBackend(object):
    type = "Example"

    def parse(self, embed):
        embed.url, embed.id = embed.raw_url.split(":")


class ExampleBackendTestCase(TestCase):
    def test_type_of_Example(self):
        backend = ExampleBackend()
        self.assertEqual("Example", backend.type)

    def test_splits_on_colon(self):
        # This test assumes that EmbeddedVideo works
        random_url = "foobar.com/watch-%d" % random.randint(100, 200)
        random_id = "%d" % random.randint(100, 200)
        backend = ExampleBackend()
        video = EmbeddedVideo("%s:%s" % (random_url, random_id), backend)

        backend.parse(video)
        self.assertEqual(video.url, random_url)
        self.assertEqual(video.id, random_id)


class EmbeddedVideoFieldTestCase(TestCase):
    def test_sets_source_to_EmbeddedVideo(self):
        video = SimpleVideoModel()
        video.source = "http://www.youtube.com/watch?v=123"
        self.assertTrue(isinstance(video.source, EmbeddedVideo))

    def test_stores_and_retrieves_from_field_from_database(self):
        random_id = "abcdef%d" % random.randint(100, 200)
        video = SimpleVideoModel.objects.create(
                source="http://youtube.com/watch?v=%s" % random_id)
        id = video.pk
        self.assertEqual(random_id,
                SimpleVideoModel.objects.get(pk=id).source.id)


class EmbeddedVideoTestCase(TestCase):
    def test_id_is_None_by_default(self):
        v = EmbeddedVideo()
        self.assertEqual(None, v.id)

    def test_settings_a_source_to_a_YouTube_url_stores_the_source_id(self):
        random_id = "abcdef%d" % random.randint(100, 200)
        video = SimpleVideoModel()
        video.source = "http://www.youtube.com/watch?v=%s" % random_id
        self.assertEqual(random_id, video.source.id)

    def test_videos_on_YouTube_have_a_source_type_of_YouTube(self):
        random_id = "abcdef%d" % random.randint(100, 200)
        video = SimpleVideoModel()
        video.source = "http://www.youtube.com/watch?v=%s" % random_id
        self.assertEqual("YouTube", video.source.type)

    def test_can_take_an_EmbeddedVideo_object_as_a_type(self):
        v = EmbeddedVideo("http://www.youtube.com/watch?v=abc")
        video = SimpleVideoModel()
        video.source = v
        self.assertEqual("YouTube", video.source.type, msg="sanity check")
        self.assertEqual("abc", video.source.id, msg="sanity check")

    def test_uses_provided_backend(self):
        random_url = "foobar-%d" % random.randint(100, 200)
        random_id = "%d" % random.randint(100, 200)
        v = EmbeddedVideo("%s:%s" % (random_url, random_id),
                backend=ExampleBackend())
        self.assertEqual(random_id, v.id)
        self.assertEqual(random_url, v.url)
        self.assertEqual("Example", v.type)

    def test_uses_configured_backend_if_nothing_is_provided(self):
        from ...video import backends
        settings = fudge.Fake()
        backend = "armstrong.core.arm_content.tests.fields.ExampleBackend"
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=backend)

        with fudge.patched_context(backends, 'default_settings', settings):
            random_url = "foobar-%d" % random.randint(100, 200)
            random_id = "%d" % random.randint(100, 200)
            v = EmbeddedVideo("%s:%s" % (random_url, random_id))
            self.assertEqual(random_id, v.id)
            self.assertEqual(random_url, v.url)

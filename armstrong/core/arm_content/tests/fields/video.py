from copy import copy
from django.db import models
import fudge
from django.utils import unittest

try:
    import south
except ImportError:
    south = False

from .._utils import *
from ..arm_content_support.models import SimpleVideoModel

from ...fields.video import EmbeddedVideo
from ... import fields
from ...video import backends


class ExampleBackend(object):
    type = "Example"

    def prepare(self, embed):
        embed.url, embed.id = embed.raw_url.split(":")


class ExampleBackendTestCase(ArmContentTestCase):
    def test_type_of_Example(self):
        backend = ExampleBackend()
        self.assertEqual("Example", backend.type)

    def test_splits_on_colon(self):
        # This test assumes that EmbeddedVideo works
        random_url = "foobar.com/watch-%d" % random.randint(100, 200)
        random_id = "%d" % random.randint(100, 200)
        backend = ExampleBackend()
        video = EmbeddedVideo("%s:%s" % (random_url, random_id), backend)

        backend.prepare(video)
        self.assertEqual(video.url, random_url)
        self.assertEqual(video.id, random_id)


class EmbeddedVideoFieldTestCase(ArmContentTestCase):
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

    def test_field_has_basic_label_by_default(self):
        field = fields.EmbeddedVideoField()
        self.assertEqual(field.formfield().label, u"Embedded Video URL")

    def test_field_can_have_custom_label_if_kwarg_provided(self):
        field = fields.EmbeddedVideoField()
        random_label = "Some random label: %d" % random.randint(100, 200)
        actual_field = field.formfield(label=random_label).label
        self.assertEqual(actual_field, random_label)

    @unittest.skipIf(south is False, "south not installed")
    def test_returns_expected_south_triple(self):
        field = fields.EmbeddedVideoField()

        expected = (
            "%s.%s" % (field.__class__.__module__, field.__class__.__name__),
            [],
            {'max_length': '255'}
        )
        self.assertEqual(field.south_field_triple(), expected)


class EmbeddedVideoTestCase(ArmContentTestCase):
    def setUp(self):
        fudge.clear_calls()
        fudge.clear_expectations()
        self.orig_backend_settings = copy(backends.backend.settings)

    def tearDown(self):
        backends.backend.settings = copy(self.orig_backend_settings)

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
        settings = fudge.Fake()
        backend = "armstrong.core.arm_content.tests.fields.ExampleBackend"
        settings.has_attr(ARMSTRONG_EXTERNAL_VIDEO_BACKEND=backend)
        backends.backend.settings = settings

        random_url = "foobar-%d" % random.randint(100, 200)
        random_id = "%d" % random.randint(100, 200)
        v = EmbeddedVideo("%s:%s" % (random_url, random_id))
        self.assertEqual(random_id, v.id)
        self.assertEqual(random_url, v.url)

    def test_embed_dispatches_to_backend_and_returns_result(self):
        random_return = random.randint(1000, 2000)
        backend = fudge.Fake()
        backend.provides("prepare")
        video = EmbeddedVideo("foo/bar", backend=backend)
        backend.expects("embed").with_args(video).returns(random_return)
        fudge.clear_calls()

        result = video.embed()
        self.assertEqual(result, random_return)

        fudge.verify()

    def test_embed_dispatches_kwargs_to_backend(self):
        kwargs = dict(
                [("key-%d" % a, a) for a in range(random.randint(1, 10))])
        backend = fudge.Fake()
        backend.provides("prepare")
        video = EmbeddedVideo("foo/bar", backend=backend)
        backend.expects("embed").with_args(video, **kwargs)
        fudge.clear_calls()

        video.embed(**kwargs)
        fudge.verify()

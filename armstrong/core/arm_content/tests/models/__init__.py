from .._utils import *
from unittest import expectedFailure

from ...models import Video


class VideoTestCase(TestCase):
    def assertVideoHasField(self, name):
        video = Video()
        self.assertTrue(hasattr(video, name),
                msg="checking that video has a field named %s" % name)

    def test_has_pub_date(self):
        self.assertVideoHasField("pub_date")

    def test_has_pub_status(self):
        self.assertVideoHasField("pub_status")

    def test_has_title(self):
        self.assertVideoHasField("title")

    def test_has_video(self):
        self.assertVideoHasField("video")

    @expectedFailure
    def test_has_authors(self):
        self.assertVideoHasField("authors")

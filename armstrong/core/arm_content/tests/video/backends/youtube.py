from ..._utils import *

from ....video import EmbeddedVideo
from ....video.backends.youtube import YouTubeBackend


class YouTubeBackendTestCase(TestCase):
    def test_returns_tuple_with_url_as_first_value(self):
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = YouTubeBackend()

        video = EmbeddedVideo(url, backend)
        self.assertEqual("http", video.url.scheme)
        self.assertEqual("youtube.com", video.url.netloc)

    def test_returns_tuple_with_id_as_second_value(self):
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = YouTubeBackend()

        video = EmbeddedVideo(url, backend)
        self.assertEqual(random_id, video.id)

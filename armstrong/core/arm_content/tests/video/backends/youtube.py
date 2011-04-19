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

    def test_returns_the_expected_html_when_embed_is_called(self):
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = YouTubeBackend()

        video = EmbeddedVideo(url, backend)
        expected = "".join([
            '<iframe title="YouTube video player" ',
            'width="640" height="390" ' ,
            'src="http://www.youtube.com/embed/%s" ',
            'frameborder="0" allowfullscreen></iframe>']) % random_id
        self.assertEqual(expected, backend.embed(video))

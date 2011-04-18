from ..._utils import *

from ....video.backends.youtube import YouTubeBackend


class YouTubeBackendTestCase(TestCase):
    def test_returns_tuple_with_url_as_first_value(self):
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = YouTubeBackend()
        (url, _id, _type) = backend.parse(url)
        self.assertEqual("http", url.scheme)
        self.assertEqual("youtube.com", url.netloc)

    def test_returns_tuple_with_id_as_second_value(self):
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = YouTubeBackend()
        (_url, id, _type) = backend.parse(url)
        self.assertEqual(random_id, id)

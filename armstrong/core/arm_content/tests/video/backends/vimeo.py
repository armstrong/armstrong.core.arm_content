from ..._utils import *

from ....video import EmbeddedVideo
from ....video.backends.vimeo import VimeoBackend


class VimeoBackendTestCase(TestCase):
    def test_prepare_sets_url_on_provided_video(self):
        backend = VimeoBackend()
        url = "http://vimeo.com/%d" % random.randint(1000, 2000)

        video = EmbeddedVideo(url, backend)
        self.assertEqual(video.url.scheme, "http")
        self.assertEqual(video.url.netloc, "vimeo.com")

    def test_prepare_sets_id_on_provided_video(self):
        random_id = str(random.randint(1000, 2000))
        backend = VimeoBackend()
        url = "http://vimeo.com/%s" % random_id

        video = EmbeddedVideo(url, backend)
        self.assertEqual(video.id, random_id)

    def test_returns_none_if_cannot_parse(self):
        unparseable_url = "foo.bar.foo:baz"
        backend = VimeoBackend()
        video = EmbeddedVideo(backend=backend)
        video.raw_url = unparseable_url

        self.assertNone(backend.prepare(video))

    def test_returns_true_if_can_parse(self):
        random_id = str(random.randint(1000, 2000))
        backend = VimeoBackend()
        url = "http://vimeo.com/%s" % random_id
        video = EmbeddedVideo(backend=backend)
        video.raw_url = url
        self.assertTrue(backend.prepare(video))

    def test_returns_none_if_video_does_not_have_raw_url(self):
        backend = VimeoBackend()
        video = EmbeddedVideo(backend=backend)
        self.assertNone(backend.prepare(video))

    def test_video_is_not_modified_if_backend_fails(self):
        backend = VimeoBackend()
        unparseable_url = "foo.bar.foo:baz"
        video = EmbeddedVideo(backend=backend)
        video.raw_url = unparseable_url

        self.assertDoesNotHave(video, "url", msg="sanity check")
        backend.prepare(video)
        self.assertDoesNotHave(video, "url")

    def test_embed_returns_expected_html_when_called(self):
        random_id = str(random.randint(1000, 2000))
        url = "http://vimeo.com/%s" % random_id
        expected_url = ''.join([
            'http://player.vimeo.com/video/%s' % random_id,
            '?title=0&amp;byline=0&amp;portrait=0'])
        expected = "".join([
            '<iframe src="%s" ' % expected_url,
            'width="398" height="224" frameborder="0"></iframe>'
        ])

        backend = VimeoBackend()
        video = EmbeddedVideo(url, backend=backend)

        self.assertEqual(backend.embed(video), expected)

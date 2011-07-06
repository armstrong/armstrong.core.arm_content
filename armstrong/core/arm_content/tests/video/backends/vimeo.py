from ..._utils import *

from ....fields.video import EmbeddedVideo
from ....video.backends import helpers
from ....video.backends import vimeo
from ....video.backends.vimeo import VimeoBackend


class VimeoBackendTestCase(ArmContentTestCase):
    def generate_random_url(self):
        random_id = random.randint(1000, 2000)
        url = "http://vimeo.com/%d" % random.randint(1000, 2000)
        return (random_id, url)

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
            'width="640" height="390" frameborder="0"></iframe>'
        ])

        backend = VimeoBackend()
        video = EmbeddedVideo(url, backend=backend)

        self.assertEqual(backend.embed(video), expected)

    def test_embed_can_change_height_with_kwarg(self):
        random_id = str(random.randint(1000, 2000))
        random_height = random.randint(1000, 2000)
        url = "http://vimeo.com/%s" % random_id
        expected_url = ''.join([
            'http://player.vimeo.com/video/%s' % random_id,
            '?title=0&amp;byline=0&amp;portrait=0'])
        expected = "".join([
            '<iframe src="%s" ' % expected_url,
            'width="398" height="%s" frameborder="0"></iframe>' \
                    % random_height,
        ])

        backend = VimeoBackend()
        video = EmbeddedVideo(url, backend=backend)

        self.assertRegexpMatches(backend.embed(video, height=random_height),
                r'height="%d"' % random_height)

    def test_embed_can_change_width_with_kwarg(self):
        random_id = str(random.randint(1000, 2000))
        random_width = random.randint(1000, 2000)
        url = "http://vimeo.com/%s" % random_id
        expected_url = ''.join([
            'http://player.vimeo.com/video/%s' % random_id,
            '?title=0&amp;byline=0&amp;portrait=0'])
        expected = "".join([
            '<iframe src="%s" ' % expected_url,
            'width="%d" height="224" frameborder="0"></iframe>' % random_width,
        ])

        backend = VimeoBackend()
        video = EmbeddedVideo(url, backend=backend)

        self.assertRegexpMatches(backend.embed(video, width=random_width),
                r'width="%d"' % random_width)

    def test_embed_width_and_height_can_be_strings(self):
        random_height = str(random.randint(1000, 2000))
        random_width = str(random.randint(1000, 2000))
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = VimeoBackend()

        url = "http://vimeo.com/%s" % random_id
        video = EmbeddedVideo(url, backend)

        self.assertRegexpMatches(backend.embed(video, width=random_width),
                r'width="%s"' % random_width)
        self.assertRegexpMatches(backend.embed(video, height=random_height),
                r'height="%s"' % random_height)

    def test_height_defaults_to_configured_if_not_provided(self):
        random_height = random.randint(1000, 2000)
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EMBED_VIDEO_HEIGHT=random_height)
        settings.has_attr(ARMSTRONG_EMBED_VIDEO_WIDTH="does not matter")

        with fudge.patched_context(helpers, 'settings', settings):
            random_id, url = self.generate_random_url()
            backend = VimeoBackend()
            video = EmbeddedVideo(url, backend)
            self.assertRegexpMatches(backend.embed(video),
                    r'height="%s"' % random_height)

    def test_width_defaults_to_configured_if_not_provided(self):
        random_width = random.randint(1000, 2000)
        settings = fudge.Fake()
        settings.has_attr(ARMSTRONG_EMBED_VIDEO_WIDTH=random_width)
        settings.has_attr(ARMSTRONG_EMBED_VIDEO_HEIGHT="does not matter")

        with fudge.patched_context(helpers, 'settings', settings):
            random_id, url = self.generate_random_url()
            backend = VimeoBackend()
            video = EmbeddedVideo(url, backend)
            self.assertRegexpMatches(backend.embed(video),
                    r'width="%s"' % random_width)

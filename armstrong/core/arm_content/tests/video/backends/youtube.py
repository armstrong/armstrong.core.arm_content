from ..._utils import *

from ....fields.video import EmbeddedVideo
from ....video.backends import helpers
from ....video.backends.youtube import YouTubeBackend


class YouTubeBackendTestCase(ArmContentTestCase):
    def generate_random_url(self):
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        return random_id, url

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
            'width="640" height="390" ',
            'src="http://www.youtube.com/embed/%s" ',
            'frameborder="0" allowfullscreen></iframe>']) % random_id
        self.assertEqual(expected, backend.embed(video))

    def test_embed_width_can_be_set_with_a_kwarg(self):
        random_width = random.randint(1000, 2000)
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = YouTubeBackend()

        video = EmbeddedVideo(url, backend)
        expected = "".join([
            '<iframe title="YouTube video player" ',
            'width="%d" height="390" ' % random_width,
            'src="http://www.youtube.com/embed/%s" ',
            'frameborder="0" allowfullscreen></iframe>']) % random_id
        self.assertRegexpMatches(backend.embed(video, width=random_width),
                r'width="%d"' % random_width)

    def test_embed_height_can_be_set_with_a_kwarg(self):
        random_height = random.randint(1000, 2000)
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = YouTubeBackend()

        video = EmbeddedVideo(url, backend)
        expected = "".join([
            '<iframe title="YouTube video player" ',
            'width="%d" height="390" ' % random_height,
            'src="http://www.youtube.com/embed/%s" ',
            'frameborder="0" allowfullscreen></iframe>']) % random_id
        self.assertRegexpMatches(backend.embed(video, height=random_height),
                r'height="%d"' % random_height)

    def test_embed_width_and_height_can_be_strings(self):
        random_height = str(random.randint(1000, 2000))
        random_width = str(random.randint(1000, 2000))
        random_id = str(random.randint(100, 200))
        url = "http://youtube.com/watch?v=%s" % random_id
        backend = YouTubeBackend()

        video = EmbeddedVideo(url, backend)
        expected = "".join([
            '<iframe title="YouTube video player" ',
            'width="%s" height="%s" ' % (random_width, random_height),
            'src="http://www.youtube.com/embed/%s" ',
            'frameborder="0" allowfullscreen></iframe>']) % random_id
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
            backend = YouTubeBackend()
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
            backend = YouTubeBackend()
            video = EmbeddedVideo(url, backend)
            self.assertRegexpMatches(backend.embed(video),
                    r'width="%s"' % random_width)

import urllib2

from .helpers import inject_defaults


class VimeoBackend(object):
    def prepare(self, embed):
        if not getattr(embed, "raw_url", False):
            return

        url = urllib2.urlparse.urlparse(embed.raw_url)
        if url.netloc[-9:] != "vimeo.com":
            return

        embed.url = url
        embed.id = url.path.lstrip("/")
        return True

    @inject_defaults
    def embed(self, embed, width=None, height=None):
        return "".join([
            '<iframe src="http://player.vimeo.com/video/%s' % embed.id,
            '?title=0&amp;byline=0&amp;portrait=0" ',
            'width="%s" height="%s" frameborder="0"></iframe>' % \
                    (width, height)
        ])

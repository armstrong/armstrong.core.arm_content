import urllib2


class YouTubeBackend(object):
    type = "YouTube"

    def prepare(self, embed):
        embed.url = urllib2.urlparse.urlparse(embed.raw_url)
        embed.id = urllib2.urlparse.parse_qs(embed.url.query)['v'][0]

    def embed(self, embed, width=640, height=390):
        # TODO: this should ultimately be a template so it can be swapped out
        return ''.join([
            '<iframe title="YouTube video player" ',
            'width="%d" height="%d" ' % (width, height),
            'src="http://www.youtube.com/embed/%s" ' % embed.id,
            'frameborder="0" allowfullscreen></iframe>'])

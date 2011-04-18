import urllib2


class YouTubeBackend(object):
    type = "YouTube"

    def parse(self, embed):
        embed.url = urllib2.urlparse.urlparse(embed.raw_url)
        embed.id = urllib2.urlparse.parse_qs(embed.url.query)['v'][0]

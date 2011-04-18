import urllib2


class YouTubeBackend(object):
    type = "YouTube"

    def parse(self, value):
        url = urllib2.urlparse.urlparse(value)
        query = urllib2.urlparse.parse_qs(url.query)['v'][0]
        return (url, query, self.type)



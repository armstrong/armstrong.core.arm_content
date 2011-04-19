import urllib2


class VimeoBackend(object):
    def prepare(self, embed):
        embed.url = urllib2.urlparse.urlparse(embed.raw_url)
        if embed.url.netloc[-9:] != "vimeo.com":
            return
        embed.id = embed.url.path.lstrip("/")
        return True

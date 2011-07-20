from .. import settings


def inject_defaults(func):
    def inner(self, embed, width=None, height=None, **kwargs):
        if not width:
            width = settings.ARMSTRONG_EMBED_VIDEO_WIDTH
        if not height:
            height = settings.ARMSTRONG_EMBED_VIDEO_HEIGHT
        return func(self, embed, width, height, **kwargs)
    return inner

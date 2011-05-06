from django.conf import settings


ARMSTRONG_EMBED_VIDEO_HEIGHT = getattr(settings,
        'ARMSTRONG_EMBED_VIDEO_HEIGHT', 390)
ARMSTRONG_EMBED_VIDEO_WIDTH = getattr(settings,
        'ARMSTRONG_EMBED_VIDEO_WIDTH', 640)

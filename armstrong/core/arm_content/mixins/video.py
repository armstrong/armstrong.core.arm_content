from django.db import models
from ..fields import EmbeddedVideoField


class EmbeddedVideoMixin(models.Model):
    video = EmbeddedVideoField()

    class Meta:
        abstract = True

from django.db import models

from . import publication
from .video import EmbeddedVideoField


class Video(publication.PublicationMixin, models.Model):
    # TODO: refactor into a TitleField
    title = models.CharField(max_length=255)
    video = EmbeddedVideoField()

    # TODO: add in authors once merge into this branch
    #authors = AuthorsField

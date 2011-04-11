from django.db import models
from polymorphic import PolymorphicModel

from ...publication.models import PublicationMixin
from ...fields import EmbeddedVideoField


class BaseContent(PolymorphicModel, PublicationMixin):
    title = models.CharField(max_length=255)


class Article(BaseContent):
    body = models.TextField()


class Video(BaseContent):
    youtube_id = models.CharField(max_length=30)


class SimpleVideoModel(models.Model):
    source = EmbeddedVideoField()

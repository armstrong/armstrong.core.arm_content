from django.db import models

from ...models import AbstractBaseContent, SubclassingManager
from ...publication.models import PublicationMixin


class BaseContent(AbstractBaseContent, PublicationMixin):
    title = models.CharField(max_length=255)

    objects = SubclassingManager()


class Article(BaseContent):
    body = models.TextField()


class Video(BaseContent):
    youtube_id = models.CharField(max_length=30)

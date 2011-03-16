from django.db import models

from ...models import AbstractBaseContent


class BaseContent(AbstractBaseContent):
    title = models.CharField(max_length=255)


class Article(BaseContent):
    body = models.TextField()


class Video(BaseContent):
    youtube_id = models.CharField(max_length=30)

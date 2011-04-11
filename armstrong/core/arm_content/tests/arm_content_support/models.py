from django.contrib.auth.models import User
from django.db import models
from polymorphic import PolymorphicModel

from ...publication.models import PublicationMixin
from ...fields import AuthorsField


class BaseContent(PolymorphicModel, PublicationMixin):
    title = models.CharField(max_length=255)


class Article(BaseContent):
    body = models.TextField()


class Video(BaseContent):
    youtube_id = models.CharField(max_length=30)


class SimpleAuthoredModel(models.Model):
    authors = AuthorsField()


class SimpleProfile(models.Model):
    user = models.OneToOneField(User)

    def get_absolute_url(self):
        return '/%s/' % self.user.get_full_name().lower().replace(' ', '-')

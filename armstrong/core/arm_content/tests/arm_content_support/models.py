from django.contrib.auth.models import User
from django.db import models

import sorl.thumbnail

from ...fields import AudioField
from ...fields import AuthorsField
from ...fields import EmbeddedVideoField
from ... import mixins
from ...mixins.images.sorl import SorlImageMixin
from ...mixins.publication import PublishedManager
from ...models import ContentBase


from armstrong.apps.content.models import Content as ConcreteContent


class ConcreteArticle(ConcreteContent):
    published = PublishedManager()


class ConcreteCommentary(ConcreteContent):
    pass


class SimpleVideoModel(models.Model):
    source = EmbeddedVideoField()


class SimpleMixedinVideoModel(mixins.EmbeddedVideoMixin, models.Model):
    pass


class SimpleAuthoredModel(models.Model):
    authors = AuthorsField()


class SimpleMixedinAuthorModel(mixins.AuthorsMixin, models.Model):
    pass


class AuthoredModelWithContentionalOverride(models.Model):
    authors = AuthorsField()
    authors_override = models.CharField(max_length=100)


class AuthoredModelWithConfiguredOverride(models.Model):
    authors = AuthorsField(override_field_name='custom_override')
    custom_override = models.CharField(max_length=100)


class AuthoredModelWithContentionalExtra(models.Model):
    authors = AuthorsField()
    authors_extra = models.CharField(max_length=100)


class AuthoredModelWithConfiguredExtra(models.Model):
    authors = AuthorsField(extra_field_name='custom_extra')
    custom_extra = models.CharField(max_length=100)


class SimpleProfile(models.Model):
    user = models.OneToOneField(User)

    def get_absolute_url(self):
        return '/%s/' % self.user.get_full_name().lower().replace(' ', '-')


class AudioModel(models.Model):
    file = AudioField(upload_to = 'audio')


class OverrideAudioModel(models.Model):
    file = AudioField(upload_to='audio')
    artist = models.CharField(max_length=100, blank=True, null=True)


class AudioMixinModel(mixins.AudioMixin): pass


class SorlImage(SorlImageMixin, models.Model):
    image = sorl.thumbnail.ImageField(upload_to='images/')

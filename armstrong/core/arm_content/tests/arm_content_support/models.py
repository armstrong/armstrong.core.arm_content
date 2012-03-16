from django.contrib.auth.models import User
from django.db import models

import sorl.thumbnail

from ...fields import AuthorsField
from ...fields import EmbeddedVideoField
from ... import mixins
from ...mixins.images.sorl import SorlThumbnailMixin
from ...mixins.publication import PublishedManager
from ...models import ContentBase


from armstrong.apps.content.models import Content as ConcreteContent


class ConcreteArticle(ConcreteContent):
    pass


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


class SorlImage(SorlThumbnailMixin, models.Model):
    image = sorl.thumbnail.ImageField(upload_to='images/')


class ContentOne(ContentBase):
    """
    This makes sure we have at least one model with sections and its reverse
    name.
    """
    pass

class ContentTwo(ContentBase):
    """
    This makes sure we have a second ContentBase sub-class that explicitly
    breaks the reverse name of the sections field.
    """
    pass

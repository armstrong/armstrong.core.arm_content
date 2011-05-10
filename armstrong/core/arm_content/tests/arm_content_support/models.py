from django.contrib.auth.models import User
from django.db import models
from polymorphic import PolymorphicModel

from ...fields import AuthorsField
from ...fields import EmbeddedVideoField
from ... import mixins
from ...mixins import PublicationMixin
from ...models import ContentBase


# for backwards compatibility -- should be removed
class BaseContent(PolymorphicModel, PublicationMixin):
    title = models.CharField(max_length=255)


class ConcreteContent(ContentBase):
    pass


class ConcreteArticle(ConcreteContent):
    pass


class ConcreteCommentary(ConcreteContent):
    pass


class Article(BaseContent):
    body = models.TextField()


class Video(BaseContent):
    youtube_id = models.CharField(max_length=30)


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

from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import InheritanceManager
from taggit.managers import TaggableManager

from . import mixins


class ContentBase(mixins.AuthorsMixin, mixins.PublicationMixin, models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()

    tags = TaggableManager()
    objects = InheritanceManager()

    # TODO: add required primary section
    # TODO: add secondary sections
    class Meta:
        abstract = True

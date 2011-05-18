from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import InheritanceManager
from taggit.managers import TaggableManager

from armstrong.core.arm_sections.managers import SectionSlugManager
from armstrong.core.arm_sections.models import Section

from . import mixins


class ContentBase(mixins.AuthorsMixin, mixins.PublicationMixin, models.Model):
    """
    The base class providing the basic "armstrong" behavior for a model.

    This is provided as a way to handle cross-model querying.  For example, you
    can use this to query across Article and Video models assuming they both
    extend from a concrete implementation of this class.

    This is *not* a concrete implementation.  This is to avoid having any
    tables created that are not needed.  `armstrong.apps.content`_ provides a
    concrete implementation of this if you want to use it without defining your
    own base Content model.

    .. _armstrong.apps.content: http://github.com/armstrongcms/armstrong.apps.content
    """

    title = models.CharField(max_length=255)
    summary = models.TextField()
    slug = models.SlugField()

    primary_section = models.ForeignKey(Section, null=True)
    sections = models.ManyToManyField(Section, null=True, blank=True,
            related_name="alternates")

    tags = TaggableManager()
    with_section = SectionSlugManager()

    objects = InheritanceManager()

    # TODO: add required primary section
    # TODO: add secondary sections
    class Meta:
        abstract = True

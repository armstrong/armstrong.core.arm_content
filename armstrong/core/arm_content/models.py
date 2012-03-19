from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import InheritanceManager
from taggit.managers import TaggableManager

from armstrong.core.arm_sections.managers import SectionSlugManager
from armstrong.core.arm_sections.models import Section
from armstrong.core.arm_access.mixins import AccessMixin

from .mixins import AuthorsMixin, PublicationMixin
from .mixins.publication import PublishedManager


class ContentBase(AuthorsMixin, PublicationMixin, AccessMixin, models.Model):
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
    # TODO: Increase max length for SlugField (see Issue #43)
    slug = models.SlugField()

    sections = models.ManyToManyField(Section, null=True, blank=True,
            related_name="%(app_label)s_%(class)s_alternates")

    tags = TaggableManager(blank=True)
    with_section = SectionSlugManager(section_field="sections")

    objects = InheritanceManager()
    published = PublishedManager()

    # TODO: add required primary section
    # TODO: add secondary sections
    class Meta:
        abstract = True

    def get_absolute_url(self):
        urlconf = __import__(settings.ROOT_URLCONF,
                             globals(),
                             locals(),
                             ['get_url_for_model'])
        return urlconf.get_url_for_model(self)

    def __unicode__(self):
        return self.title

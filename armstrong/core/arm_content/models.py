from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet

from .constants import PUB_STATUS_CHOICES


class AbstractBaseContent(models.Model):
    '''
    Provides the fields necessary to determine whether an item will appear on the site.

    To pull the latest content from across the site, there must be a common
    model for us to query that all of the desired content items inherit from.
    The fields in AbstractBaseContent are the fields tht would be used in such
    a query. The overarching content model used in an Armstrong implementation
    should contain these fields.
    '''
    pub_date = models.DateTimeField(db_index=True)
    pub_status = models.CharField((u'Publication status'), max_length=1,
        choices=PUB_STATUS_CHOICES, help_text=(u'Only published items will appear on the site'))
    # Subclasses keep track of their content type here so the original
    # subclassed object can be obtained given a BaseContent row from the DB.
    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(AbstractBaseContent, self).save(*args, **kwargs)

    def as_child_class(self):
        if not hasattr(self, '_child_obj'):
            self._child_obj = self.content_type.get_object_for_this_type(pk=self.pk)
        return self._child_obj


class SubclassingQuerySet(QuerySet):
    '''
    Yields the child class version object for each item.

    Requires a model that has as_child_class method that does the actual work.
    Inspired by: http://www.djangosnippets.org/snippets/1034/
    '''
    # TODO: When a queryset is evaluated, we should try to pull all items of
    # each type at the same time to use fewer queries.
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_child_class()
        else:
            return result

    def iterator(self):
        for item in super(SubclassingQuerySet, self).iterator():
            child = item.as_child_class()
            # When an error occurs while creating a Content item, the
            # Content item may have already been created without the
            # subclass creation succeeding. Ignore those.
            if child is not None:
                yield child


class SubclassingManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)

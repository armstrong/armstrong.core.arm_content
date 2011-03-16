from django.db import models

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

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

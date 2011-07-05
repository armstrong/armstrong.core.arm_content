from django.db import models
from ..fields import AuthorsField


class AuthorsMixin(models.Model):
    authors = AuthorsField(blank=True)
    authors_extra = models.CharField(blank=True, max_length=200)
    authors_override = models.CharField(blank=True, max_length=200)

    class Meta:
        abstract = True

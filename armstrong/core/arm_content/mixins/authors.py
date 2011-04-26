from django.db import models
from ..fields import AuthorsField


class AuthorsMixin(models.Model):
    authors = AuthorsField()
    authors_extra = models.CharField(max_length=200)
    authors_override = models.CharField(max_length=200)

    class Meta:
        abstract = True

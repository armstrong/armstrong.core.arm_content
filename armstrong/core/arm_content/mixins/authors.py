from django.db import models
from ..fields import AuthorsField


class AuthorsMixin(object):
    authors = AuthorsField()
    authors_extra = models.CharField(max_length=200)
    authors_override = models.CharField(max_length=200)

from django.db import models

from ..models import Authors


class AuthorsField(models.ManyToManyField):
    pass

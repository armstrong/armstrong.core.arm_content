from django.db import models

from ..models import Authors


class AuthorsField(models.OneToOneField):
    def __init__(self, **kwargs):
        super(AuthorsField, self).__init__(Authors, **kwargs)

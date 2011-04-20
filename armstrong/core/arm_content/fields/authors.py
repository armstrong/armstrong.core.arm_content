from django.db import models

from ..models import Authors
from ..authors.forms import AuthorsFormField


class AuthorsField(models.OneToOneField):
    def __init__(self, **kwargs):
        super(AuthorsField, self).__init__(Authors, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"form_class": AuthorsFormField}
        defaults.update(kwargs)
        return super(AuthorsField, self).formfield(**defaults)

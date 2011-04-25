from django.db import models
from .._utils import *
from ...fields import AuthorsField
from ...mixins import AuthorsMixin


class SimpleAuthoredModel(AuthorsMixin, models.Model):
    pass

class AuthorsMixinTestCase(TestCase):
    def assertModelHasField(self, model, field_name, field_class):
        self.assertTrue(hasattr(model, field_name))
        self.assertTrue(isinstance(getattr(model, field_name), field_class))

    def test_models_mixed_in_with_AuthorsMixin_have_an_authors_field(self):
        model = SimpleAuthoredModel()
        self.assertModelHasField(model, "authors", AuthorsField)

    def test_has_authors_extra_field(self):
        model = SimpleAuthoredModel()
        self.assertModelHasField(model, "authors_extra", models.CharField)

    def test_has_authors_override_field(self):
        model = SimpleAuthoredModel()
        self.assertModelHasField(model, "authors_override", models.CharField)

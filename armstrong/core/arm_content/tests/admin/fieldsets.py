from .._utils import *

from ...admin import fieldsets

class FieldSetFactoryTestCase(TestCase):
    fieldset_factory = None

    @property
    def is_not_runnable(self):
        return self.fieldset_factory is None

    def setUp(self):
        if self.is_not_runnable:
            return
        self.fieldset = getattr(fieldsets, self.fieldset_factory)()

    def test_expected_title(self):
        if self.is_not_runnable:
            return
        title, options = self.fieldset
        self.assertEqual(self.expected_title, title)

    def test_contains_expected_fields(self):
        if self.is_not_runnable:
            return
        fields = self.fieldset[1]["fields"]
        for field_name in self.expected_fields:
            self.assertTrue(field_name in fields, msg="checking for %s field")


class PublicationFieldSet(FieldSetFactoryTestCase):
    fieldset_factory = 'publication'
    expected_title = "Publication Information"
    expected_fields = ("pub_date", "pub_status", "sites", )


class AuthorsFieldSetTestCase(FieldSetFactoryTestCase):
    fieldset_factory = 'authors'
    expected_title = "Author Information"
    expected_fields = ('authors', 'authors_override', 'authors_extra' )

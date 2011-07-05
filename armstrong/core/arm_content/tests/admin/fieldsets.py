from .._utils import *

from ...admin import fieldsets


class FieldSetFactoryTestCase(ArmContentTestCase):
    fieldset_name = None

    @property
    def is_not_runnable(self):
        return self.fieldset_name is None

    def setUp(self):
        if self.is_not_runnable:
            return
        self.fieldset = getattr(fieldsets, self.fieldset_name)

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
    fieldset_name = 'PUBLICATION'
    expected_title = "Publication Information"
    expected_fields = ("pub_date", "pub_status", "sites", )


class AuthorsFieldSetTestCase(FieldSetFactoryTestCase):
    fieldset_name = 'AUTHORS'
    expected_title = "Author Information"
    expected_fields = ('authors', 'authors_override', 'authors_extra', )

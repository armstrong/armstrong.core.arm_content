from .._utils import *
from fudge import Fake, patched_context
from fudge.inspector import arg
import random
import re

from ...authors import forms


def dict_contains(expected):
    def inner(value):
        return expected in value
    return inner


class dict_containsTestCase(TestCase):
    def test_returns_true_if_dict_contains_value(self):
        d = {"foo": False}
        self.assertTrue(dict_contains("foo")(d))

    def test_returns_false_if_dict_does_not_contain_value(self):
        d = {"foo": False}
        self.assertFalse(dict_contains("bar")(d))


class AuthorsWidgetTestCase(TestCase):
    def assertContextContains(self, expected):
        render_to_string = Fake(callable=True)
        render_to_string.with_args(arg.any(),
                arg.passes_test(dict_contains(expected)))
        with patched_context(forms, "render_to_string", render_to_string):
            w = forms.AuthorsWidget()
            w.render(None, None)

    def assertContainsHtml(self, html, string):
        self.assertTrue(re.search(r"%s" % html, string) is not None)

    def test_provides_override_widget_to_context(self):
        self.assertContextContains("override_widget")

    def test_provides_extra_widget_to_context(self):
        self.assertContextContains("extra_widget")

    def test_provides_staff_widget_to_context(self):
        self.assertContextContains("staff_widget")

    def test_prefixes_fields_with_name_provided(self):
        random_name = "some-random-name-%d" % random.randint(100, 200)
        w = forms.AuthorsWidget()
        result = w.render(random_name, None)

        self.assertEqual(len(re.findall(r"%s_" % random_name, result)), 3)

    def test_contains_multi_select_with_staff_as_authors(self):
        bob, alice = generate_random_staff_users()
        w = forms.AuthorsWidget()
        result = w.render("authors", None)

        self.assertContainsHtml(
                '<select multiple="multiple" name="authors__users">',
                result)

    def test_ignores_non_staff_members_in_authors_list(self):
        bob, alice = generate_random_staff_users()
        travis, niran = generate_random_users()

        w = forms.AuthorsWidget()
        result = w.render("authors", None)

        self.assertRegexpMatches(
                result, r'<option value="%d">%s</option>' % (bob.pk, bob))
        self.assertRegexpMatches(
                result, r'<option value="%d">%s</option>' % (alice.pk, alice))
        self.assertNotRegexpMatches(
                result, r'<option value="%d">%s</option>' % (travis.pk, travis))
        self.assertNotRegexpMatches(
                result, r'<option value="%d">%s</option>' % (niran.pk, niran))

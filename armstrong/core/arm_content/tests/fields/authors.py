# coding=utf-8
import fudge

from ..arm_content_support.models import AuthoredModelWithConfiguredOverride
from ..arm_content_support.models import AuthoredModelWithContentionalOverride
from ..arm_content_support.models import AuthoredModelWithConfiguredExtra
from ..arm_content_support.models import AuthoredModelWithContentionalExtra
from ..arm_content_support.models import SimpleAuthoredModel
from ..arm_content_support.models import SimpleProfile
from .._utils import *

from ...fields import authors


def add_authors_to(model, *authors):
    for author in authors:
        model.authors.add(author)


def random_authored_model(klass, *authors):
    article = klass.objects.create()
    add_authors_to(article, *authors)
    return article


class AuthorsFieldTestCase(TestCase):
    def test_authors_fields_are_contain_all_users_when_cast_to_string(self):
        bob, alice = generate_random_staff_users()
        article = random_authored_model(SimpleAuthoredModel, bob, alice)

        expected = "%s and %s" % (bob.get_full_name(), alice.get_full_name())
        self.assertEqual(str(article.authors), expected)

    def test_should_be_able_to_convert_to_unicode(self):
        bob, alice = generate_random_staff_users()
        bob.first_name = u"Bøb"
        bob.save()
        article = random_authored_model(SimpleAuthoredModel, bob, alice)

        self.assertTrue(type(article.authors.__unicode__()) is unicode)
        expected = "%s and %s" % (bob.get_full_name(), alice.get_full_name())
        self.assertEqual(article.authors.__unicode__(), expected)

    def test_override_changes_the_string_output(self):
        override = "This is a random override %d" % random.randint(1000, 2000)
        bob, alice = generate_random_staff_users()

        article = random_authored_model(AuthoredModelWithContentionalOverride,
                bob, alice)
        article.authors_override = override

        self.assertEqual(str(article.authors), override)

    def test_override_can_be_configured(self):
        # TODO: dynamically generate this model and use a random name
        override = "This is a random override %d" % random.randint(1000, 2000)
        bob, alice = generate_random_staff_users()

        article = random_authored_model( AuthoredModelWithConfiguredOverride,
                bob, alice)
        add_authors_to(article, bob, alice)
        article.custom_override = override

        self.assertEqual(str(article.authors), override)

    def test_extra_is_appended_to_the_end(self):
        extra = "extra %d data" % random.randint(1000, 2000)
        bob, alice = generate_random_staff_users()

        article = random_authored_model(AuthoredModelWithContentionalExtra,
                bob, alice)
        article.authors_extra = extra
        expected = "%s, %s %s" % (bob.get_full_name(),
                alice.get_full_name(), extra)
        self.assertEqual(str(article.authors), expected)

    def test_extra_field_can_be_configured(self):
        extra = "extra %d data" % random.randint(1000, 2000)
        bob, alice = generate_random_staff_users()

        article = random_authored_model(AuthoredModelWithConfiguredExtra,
                bob, alice)
        article.custom_extra = extra
        expected = "%s, %s %s" % (bob.get_full_name(),
                alice.get_full_name(), extra)
        self.assertEqual(str(article.authors), expected)

    def test_separates_all_but_last_two_users_with_commas(self):
        bob, alice = generate_random_staff_users()
        r = random.randint(1, 3)
        extra_authors = generate_random_staff_users(n=r)

        article = random_authored_model(SimpleAuthoredModel, bob, alice,
                *extra_authors)

        self.assertEqual(r, str(article.authors).count(','))
        self.assertEqual(1, str(article.authors).count(' and '),
                msg="sanity check")


    def test_html_returns_plain_list_if_not_configured_with_profiles(self):
        bob, alice = generate_random_staff_users()
        expected = "%s and %s" % (bob.get_full_name(), alice.get_full_name())
        article = random_authored_model(SimpleAuthoredModel, bob, alice)

        settings = fudge.Fake()
        settings.has_attr(AUTH_PROFILE_MODULE=None)
        with fudge.patched_context(authors, 'settings', settings):
            self.assertEqual(article.authors.html(), expected)

    def test_html_returns_string_with_html_links(self):
        bob, alice = generate_random_staff_users()
        article = random_authored_model(SimpleAuthoredModel, bob, alice)
        add_profile_to(SimpleProfile, bob, alice)
        expected_html_links = [
                '<a href="/%s/">%s</a>' % (
                    bob.get_full_name().lower().replace(' ', '-'),
                    bob.get_full_name()),
                '<a href="/%s/">%s</a>' % (
                    alice.get_full_name().lower().replace(' ', '-'),
                    alice.get_full_name()),
        ]
        expected = ' and '.join(expected_html_links)
        self.assertEqual(article.authors.html(), expected)

    def test_alpha_spacing_of_extra(self):
        bob, alice = generate_random_staff_users()
        article = random_authored_model(AuthoredModelWithContentionalExtra,
                bob, alice)
        extra = "space expected before the s"
        article.authors_extra = extra
        expected = "%s, %s %s" % (bob.get_full_name(), alice.get_full_name(),
                extra)
        self.assertEqual(str(article.authors), expected)

    def test_no_spacing_with_non_alpha_on_extras(self):
        bob, alice = generate_random_staff_users()
        article = random_authored_model(AuthoredModelWithContentionalExtra,
                bob, alice)
        extra = ", no space expected before the s"
        article.authors_extra = extra
        expected = "%s, %s%s" % (bob.get_full_name(), alice.get_full_name(),
                extra)
        self.assertEqual(str(article.authors), expected)

# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils import unittest
from django.template import Template, Context
import fudge
try:
    import south
except ImportError:
    south = False

from ..arm_content_support.models import AuthoredModelWithConfiguredOverride
from ..arm_content_support.models import AuthoredModelWithContentionalOverride
from ..arm_content_support.models import AuthoredModelWithConfiguredExtra
from ..arm_content_support.models import AuthoredModelWithContentionalExtra
from ..arm_content_support.models import SimpleAuthoredModel
from ..arm_content_support.models import SimpleProfile
from .._utils import *

from ...fields import authors


class AuthorsFieldTestCase(ArmContentTestCase):
    def test_authors_can_have_one_author(self):
        [bob, ] = generate_random_staff_users(n=1)
        article = SimpleAuthoredModel.objects.create()
        article.authors.add(bob)

        self.assertEqual(bob.get_full_name(), str(article.authors))

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

    def test_override_is_ignored_if_empty(self):
        empty_override = ""
        bob, alice = generate_random_staff_users()

        article = random_authored_model(AuthoredModelWithContentionalOverride,
                bob, alice)
        article.authors_override = empty_override

        expected = "%s and %s" % (bob.get_full_name(), alice.get_full_name())
        self.assertEqual(str(article.authors), expected)

    def test_override_can_be_configured(self):
        # TODO: dynamically generate this model and use a random name
        override = "This is a random override %d" % random.randint(1000, 2000)
        bob, alice = generate_random_staff_users()

        article = random_authored_model(AuthoredModelWithConfiguredOverride,
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

    @unittest.skipIf(south is False, "south not installed")
    def test_provides_south_field_triple(self):
        field = authors.AuthorsField()
        expected = (
            "%s.%s" % (field.__class__.__module__, field.__class__.__name__),
            [],
            {
                "to": "orm['auth.User']",
                "override_field_name": "'authors_override'",
                "extra_field_name": "'authors_extra'",
                "symmetrical": "False",
            })
        self.assertEqual(field.south_field_triple(), expected)

    def test_defaults_to_being_related_to_base_user(self):
        field = authors.AuthorsField()
        self.assertEqual(field.rel.to, User)

    def test_can_relate_to_custom_user(self):
        class MyUser(models.Model):
            pass

        field = authors.AuthorsField(to=MyUser)
        self.assertEqual(field.rel.to, MyUser)

    def test_can_render_in_templates(self):
        [bob, ] = generate_random_staff_users(n=1)
        article = SimpleAuthoredModel.objects.create()
        article.authors.add(bob)
        t = Template("{{ article.authors }}")
        context = Context({"article": article})
        self.assertEqual(bob.get_full_name(), t.render(context))



class AuthorsDescriptorTestCase(ArmContentTestCase):
    def test_does_not_choke_on_empty_instance(self):
        try:
            authors_field = SimpleAuthoredModel.authors
            self.assertTrue(True, "Was able to look at authors on the model")
        except AttributeError, e:
            self.fail("Should not have raised an exception: %s" % e)

    def test_returns_descriptor_when_retrieved_off_of_model(self):
        authors_field = SimpleAuthoredModel.authors
        self.assertTrue(isinstance(authors_field, authors.AuthorsDescriptor))

    def test_can_accept_being_set_to_a_list(self):
        article = SimpleAuthoredModel.objects.create()
        staff = generate_random_staff_users(n=2)
        article.authors = staff
        self.assertTrue(type(article.authors) is not list)

    def test_has_the_same_users_after_being_set_to_list(self):
        article = SimpleAuthoredModel.objects.create()
        staff = generate_random_staff_users(n=2)
        article.authors = staff

        self.assertEqual(article.authors.all().count(), len(staff))
        for author in article.authors.all():
            self.assertTrue(author in staff)

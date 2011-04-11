from django.contrib.auth.models import User
import fudge
import random

from ..arm_content_support.models import SimpleProfile
from .._utils import *

from ...models import Authors
from ... import models


def generate_random_user():
    r = random.randint(10000, 20000)
    return User.objects.create(username="random-user-%d" % r,
            first_name="Some", last_name="Random User %d" % r)


def generate_random_users(n=2):
    return [generate_random_user() for i in range(n)]


def add_n_users_to_authors(authors, *users):
    for user in users:
        authors.users.add(user)


def add_profile_to(profile_class, *users):
    for user in users:
        profile = profile_class.objects.create(user=user)
        user._profile_cache = profile


def generate_authors_with_two_users():
    authors = Authors.objects.create()
    bob, alice = generate_random_users()
    add_n_users_to_authors(authors, bob, alice)
    return authors, bob, alice


class AuthorsModelTestCase(TestCase):
    def test_should_include_all_users_when_cast_to_a_string(self):
        authors, bob, alice = generate_authors_with_two_users()
        expected = "%s and %s" % (bob.get_full_name(), alice.get_full_name())
        self.assertEqual(expected, str(authors))

    def test_override_changes_the_string_output(self):
        override = "This is a random override %d" % random.randint(1000, 2000)
        authors, bob, alice = generate_authors_with_two_users()
        authors.override = override
        self.assertEqual(override, str(authors))

    def test_extra_is_appended_to_the_end(self):
        extra = "extra %d data" % random.randint(1000, 2000)
        authors, bob, alice = generate_authors_with_two_users()
        authors.extra = extra
        expected = "%s and %s %s" % (bob.get_full_name(),
                alice.get_full_name(), extra)
        self.assertEqual(expected, str(authors))

    def test_separates_all_but_last_two_users_with_commas(self):
        authors, bob, alice = generate_authors_with_two_users()
        r = random.randint(1, 3)
        extra_authors = generate_random_users(n=r)
        add_n_users_to_authors(authors, *extra_authors)

        self.assertEqual(r, str(authors).count(','))
        self.assertEqual(1, str(authors).count(' and '), msg="sanity check")

    def test_html_returns_plain_list_if_not_configured_with_profiles(self):
        authors, bob, alice = generate_authors_with_two_users()
        expected = "%s and %s" % (bob.get_full_name(), alice.get_full_name())

        settings = fudge.Fake(models.settings)
        settings.has_attr(AUTH_PROFILE_MODULE=None)
        with fudge.patched_context(models, 'settings', settings):
            self.assertEqual(expected, authors.html())

    def test_html_returns_string_with_html_links(self):
        authors, bob, alice = generate_authors_with_two_users()
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
        self.assertEqual(expected, authors.html())

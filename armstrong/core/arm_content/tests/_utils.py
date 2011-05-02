from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
import fudge
import random
import unittest

from .arm_content_support.models import Article, Video
from ..publication.constants import PUB_STATUSES


class TestCase(DjangoTestCase):
    def setUp(self):
        fudge.clear_expectations()
        fudge.clear_calls()

    def assertModelHasField(self, model, field_name, field_class=None):
        self.assertTrue(hasattr(model, field_name))
        field = model._meta.get_field_by_name(field_name)[0]
        if field_class is not None:
            self.assertTrue(isinstance(field, field_class))

    def assertNone(self, obj, **kwargs):
        self.assertTrue(obj is None, **kwargs)

    def assertIsA(self, obj, cls, **kwargs):
        self.assertTrue(isinstance(obj, cls), **kwargs)

    def assertDoesNotHave(self, obj, attr, **kwargs):
        self.assertFalse(hasattr(obj, attr), **kwargs)

def create_random_article(**options):
    random_int = random.randint(1000, 9999)
    data = {
        'pub_date': datetime.now(),
        'pub_status': PUB_STATUSES['Published'],
        'title': 'Random Article %s' % random_int,
        'body': str(random_int),
    }
    data.update(options)
    return Article.objects.create(**data)

def create_random_video(**options):
    random_int = random.randint(1000, 9999)
    data = {
        'pub_date': datetime.now(),
        'pub_status': PUB_STATUSES['Published'],
        'title': 'Random Article %s' % random_int,
        'youtube_id': str(random_int),
    }
    data.update(options)
    return Video.objects.create(**data)


def generate_random_user():
    r = random.randint(10000, 20000)
    return User.objects.create(username="random-user-%d" % r,
            first_name="Some", last_name="Random User %d" % r)


def generate_random_staff_users(n=2):
    orig_users = generate_random_users(n)
    users = User.objects.filter(pk__in=[a.id for a in orig_users])
    users.update(is_staff=True)
    return [a for a in users]

class generate_random_staff_usersTestCase(TestCase):
    def test_returns_2_users_by_default(self):
        self.assertEqual(len(generate_random_staff_users()), 2)

    def test_returns_n_users(self):
        r = random.randint(1, 5)
        self.assertEqual(len(generate_random_staff_users(r)), r)

    def test_all_users_are_staff(self):
        users = generate_random_staff_users()
        for user in users:
            self.assertTrue(user.is_staff)

def generate_random_users(n=2):
    return [generate_random_user() for i in range(n)]


def add_n_users_to_authors(authors, *users):
    for user in users:
        authors.users.add(user)


def add_profile_to(profile_class, *users):
    for user in users:
        profile = profile_class.objects.create(user=user)
        user._profile_cache = profile

def add_authors_to(model, *authors):
    for author in authors:
        model.authors.add(author)

def random_authored_model(klass, *authors):
    article = klass.objects.create()
    add_authors_to(article, *authors)
    return article

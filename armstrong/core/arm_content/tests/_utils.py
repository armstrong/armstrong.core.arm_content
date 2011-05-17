from datetime import datetime
from django.contrib.auth.models import User
from django.core.management.color import no_style
from django.db import connection
from django.db import models
from django.test import TestCase as DjangoTestCase
from django.utils import unittest
import fudge
import random

from .arm_content_support.models import Article, Video
from ..mixins.publication import PUB_STATUSES


def create_concrete_table(func=None, model=None):
    style = no_style()
    seen_models = connection.introspection.installed_models(
            connection.introspection.table_names())

    def actual_create(model):
        sql, _references = connection.creation.sql_create_model(model, style,
                seen_models)
        cursor = connection.cursor()
        for statement in sql:
            cursor.execute(statement)

    if func:
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            actual_create(self.model)
        return inner
    elif model:
        actual_create(model)


def destroy_concrete_table(func=None, model=None):
    style = no_style()
    # Assume that there are no references to destroy, these are supposed to be
    # simple models
    references = {}

    def actual_destroy(model):
        sql = connection.creation.sql_destroy_model(model, references, style)
        cursor = connection.cursor()
        for statement in sql:
            cursor.execute(statement)

    if func:
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            actual_destroy(self.model)
        return inner
    elif model:
        actual_destroy(model)


# TODO: pull into a common dev package so all armstrong code can use it
def concrete(klass):
    attrs = {'__module__': concrete.__module__, }
    while True:
        num = random.randint(1, 10000)
        if num not in concrete.already_used:
            break
    return type("Concrete%s%d" % (klass.__name__, num), (klass, ), attrs)
concrete.already_used = []


class TestCase(DjangoTestCase):
    def setUp(self):
        fudge.clear_expectations()
        fudge.clear_calls()

    def assertRelatedTo(self, model, field_name, related_model, many=False):
        if many is False:
            through = models.ForeignKey
        else:
            through = models.ManyToManyField

        # sanity check
        self.assertModelHasField(model, field_name, through)

        field = model._meta.get_field_by_name(field_name)[0]
        self.assertEqual(field.rel.to, related_model)

    def assertModelHasField(self, model, field_name, field_class=None):
        msg = "%s does not have a field named %s" % (model.__class__.__name__,
                field_name)
        self.assertTrue(hasattr(model, field_name), msg=msg)
        field = model._meta.get_field_by_name(field_name)[0]
        if field_class is not None:
            msg = "%s.%s is not a %s" % (model.__class__.__name__, field_name,
                    field_class.__class__.__name__)
            self.assertTrue(isinstance(field, field_class), msg=msg)

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

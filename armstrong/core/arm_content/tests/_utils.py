from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
import random

from .arm_content_support.models import Article, Video
from ..models import Authors
from ..publication.constants import PUB_STATUSES


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

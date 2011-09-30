from datetime import datetime
from django.core.files import File
from django.conf import settings

from armstrong.dev.tests.utils import ArmstrongTestCase
from armstrong.dev.tests.utils.concrete import *
from armstrong.dev.tests.utils.users import *

import fudge


class ArmContentTestCase(ArmstrongTestCase):
    pass


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

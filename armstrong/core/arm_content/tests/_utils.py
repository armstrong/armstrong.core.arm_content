from datetime import datetime
from django.test import TestCase as DjangoTestCase
import fudge
import random

from .arm_content_support.models import Article, Video
from ..publication.constants import PUB_STATUSES


class TestCase(DjangoTestCase):
    def setUp(self):
        fudge.clear_expectations()
        fudge.clear_calls()

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

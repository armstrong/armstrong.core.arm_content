# coding=utf-8
from django.db import models
from .._utils import *

from ..arm_content_support.models import ConcreteArticle

import datetime

class PublicationManagerTestCase(ArmContentTestCase):
    def setUp(self):
        self.published = ConcreteArticle.objects.create(
                title="Published",
                pub_date=datetime.datetime.now()-datetime.timedelta(days=1),
                pub_status='P'
            )
        self.draft_art = ConcreteArticle.objects.create(
                title="Not Published",
                pub_date=datetime.datetime.now()-datetime.timedelta(days=1),
                pub_status='D'
            )
        self.scheduled = ConcreteArticle.objects.create(
                title="Future Published",
                pub_date=datetime.datetime.now()+datetime.timedelta(days=1),
                pub_status='P'
            )

    def test_published_manager_only_pulls_published_content(self):
        all_published = ConcreteArticle.published.all().select_subclasses()
        self.assertTrue(self.published in all_published)
        self.assertTrue(not self.draft_art in all_published)
        self.assertTrue(not self.scheduled in all_published)

    def test_is_published(self):
        self.assertTrue(self.published.is_published)
        self.assertFalse(self.draft_art.is_published)
        self.assertFalse(self.scheduled.is_published)
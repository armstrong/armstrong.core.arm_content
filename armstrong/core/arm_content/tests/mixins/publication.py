# coding=utf-8
from django.db import models
from .._utils import *

from ..arm_content_support.models import ConcreteArticle
from ...models import ContentBase

import datetime

class PublicationManagerTestCase(ArmContentTestCase):
    def test_ContentBase_subclasses_have_published_manager(self):
        class ConcreteContent(ContentBase):
            pass
        self.assertTrue(hasattr(ConcreteContent, 'published'))

    def test_subclasses_of_concrete_classes_have_published_manager(self):
        class ConcreteContent(ContentBase):
            pass
        class ConcreteArticle(ConcreteContent):
            pass
        self.assertTrue(hasattr(ConcreteArticle, 'published'))

    def test_published_manager_only_pulls_published_content(self):
        published = ConcreteArticle.objects.create(title="Published",
                                           pub_date=datetime.datetime.now()-datetime.timedelta(days=1),
                                           pub_status='P')
        draft_art = ConcreteArticle.objects.create(title="Not Published",
                                           pub_date=datetime.datetime.now()-datetime.timedelta(days=1),
                                           pub_status='D')
        scheduled = ConcreteArticle.objects.create(title="Future Published",
                                           pub_date=datetime.datetime.now()+datetime.timedelta(days=1),
                                           pub_status='P')
        all_published = ConcreteArticle.published.all().select_subclasses()
        self.assertTrue(published in all_published)
        self.assertTrue(not draft_art in all_published)
        self.assertTrue(not scheduled in all_published)

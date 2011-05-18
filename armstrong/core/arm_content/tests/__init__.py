from ._utils import TestCase, create_random_article, create_random_video
from .arm_content_support.models import BaseContent, Article, Video
from .admin import *
from .fields import *
from .mixins import *
from .models import *
from .video import *


class BaseContentTestCase(TestCase):
    def test_can_add_content(self):
        article = create_random_article()
        Article.objects.get(id=article.id)

    def test_can_fetch_combined_queryset(self):
        create_random_article()
        create_random_video()
        create_random_article()
        create_random_video()

        self.assertEqual(BaseContent.objects.count(), 4)
        for item in BaseContent.objects.all():
            self.assertFalse(item.__class__ == BaseContent)

        articles = [item for item in BaseContent.objects.all() if
            item.__class__ == Article]
        self.assertEqual(len(articles), 2)

        videos = [item for item in BaseContent.objects.all() if
            item.__class__ == Video]
        self.assertEqual(len(videos), 2)

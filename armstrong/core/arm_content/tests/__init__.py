from django.test import TestCase

from .arm_content_support.models import Article, Video
from ._utils import create_random_article


class AbstractBaseContentTestCase(TestCase):
    def test_can_add_content(self):
        article = create_random_article()
        Article.objects.get(id=article.id)

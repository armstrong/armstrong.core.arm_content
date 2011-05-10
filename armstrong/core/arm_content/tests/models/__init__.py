from .._utils import *
import datetime
from django.db import models
from taggit.managers import TaggableManager

from ..arm_content_support.models import ConcreteArticle
from ..arm_content_support.models import ConcreteCommentary
from ..arm_content_support.models import ConcreteContent
from ...models import ContentBase

now = datetime.datetime.now


class ContentBaseTestCase(TestCase):
    @create_concrete_table
    def setUp(self):
        self.model = concrete(ContentBase)

    @destroy_concrete_table
    def tearDown(self):
        pass

    def test_has_a_title(self):
        self.assertModelHasField(self.model(), "title", models.CharField)

    def test_has_summary(self):
        self.assertModelHasField(self.model(), "summary", models.TextField)

    def test_has_tags(self):
        # Must create a full model here so we have a pk for tags to be
        # associated with
        model = self.model.objects.create(pub_date=now(),
                pub_status="Published")
        self.assertModelHasField(model, "tags", TaggableManager)


class ConcreteContentBaseTestCase(TestCase):
    def setUp(self):
        self.some_model = ConcreteArticle
        self.another_model = ConcreteCommentary

    def test_can_retrieve_all_models_as_part_of_parent_class(self):
        one = self.some_model.objects.create(pub_date=now(),
                pub_status="Published")
        two = self.another_model.objects.create(pub_date=now(),
                pub_status="Published")

        self.assertEqual(ConcreteContent.objects.all().count(), 2)
        pub_dates = [a.pub_date for a in ConcreteContent.objects.all()]
        self.assertTrue(one.pub_date in pub_dates)
        self.assertTrue(two.pub_date in pub_dates)

    def test_only_uses_one_query_to_get_subclasses(self):
        one = self.some_model.objects.create(pub_date=now(),
                pub_status="Published")
        two = self.another_model.objects.create(pub_date=now(),
                pub_status="Published")

        self.assertNotEqual(one.__class__, two.__class__, msg="sanity check")
        with self.assertNumQueries(1):
            subclass_queryset = ConcreteContent.objects.select_subclasses()
            [alt_one, alt_two] = subclass_queryset.all()
            self.assertEqual(alt_one.__class__, one.__class__)
            self.assertEqual(alt_two.__class__, two.__class__)

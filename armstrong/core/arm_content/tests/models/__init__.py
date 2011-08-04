from .._utils import *
import datetime
from django.db import models
from taggit.managers import TaggableManager

from armstrong.core.arm_sections.models import Section
from ..arm_content_support.models import ConcreteArticle
from ..arm_content_support.models import ConcreteCommentary
from ..arm_content_support.models import ConcreteContent
from ...models import ContentBase
from ...models import Section

now = datetime.datetime.now


class ContentBaseTestCase(ArmContentTestCase):
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

    def test_has_slug(self):
        self.assertModelHasField(self.model(), "slug", models.SlugField)

    def test_has_tags(self):
        # Must create a full model here so we have a pk for tags to be
        # associated with
        model = self.model.objects.create(pub_date=now(),
                pub_status="Published")
        self.assertModelHasField(model, "tags", TaggableManager)

    def test_has_sections(self):
        model = self.model.objects.create(pub_date=now(),
                pub_status="Published")
        self.assertRelatedTo(model, "sections", Section, many=True)


class ConcreteContentBaseTestCase(ArmContentTestCase):
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

    def test_can_grab_by_full_slug(self):
        title = "Random Title %d" % random.randint(100, 200)
        slug = "random-%d" % random.randint(100, 200)
        article_slug = "some-random-article-slug-%d" % random.randint(100, 200)
        section = Section.objects.create(title="Random", slug=slug)
        m = self.some_model.objects.create(title=title, pub_date=now(),
                slug=article_slug, pub_status="Published")
        m.sections.add(section)

        article = self.some_model.with_section.get_by_slug("%s/%s" % (slug,
            article_slug))

        self.assertEqual(article.title, title)

    def test_can_grab_by_full_slug_if_in_nested_section(self):
        title = "Random Title %d" % random.randint(100, 200)
        slug = "random-%d" % random.randint(100, 200)
        article_slug = "some-random-article-slug-%d" % random.randint(100, 200)
        section = Section.objects.create(title="Random", slug=slug)
        child = Section.objects.create(title="Random Child", slug=slug,
                parent=section)
        m = self.some_model.objects.create(title=title, pub_date=now(),
                slug=article_slug, pub_status="Published")
        m.sections.add(child)

        article = self.some_model.with_section.get_by_slug("%s%s" %
                (child.full_slug, article_slug))

        self.assertEqual(article.title, title)

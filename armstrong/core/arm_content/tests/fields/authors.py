from ..arm_content_support.models import SimpleAuthoredModel
from .._utils import *

from ...models import Authors


class AuthorsFieldTestCase(TestCase):
    def test_authors_fields_are_Authors_models_when_converted_to_python(self):
        authors, bob, alice = generate_authors_with_two_users()
        article = SimpleAuthoredModel.objects.create(authors=authors)

        self.assertTrue(isinstance(article.authors, Authors))

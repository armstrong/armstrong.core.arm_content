from .._utils import *
from django.core.urlresolvers import reverse

from .fieldsets import *


class AuthorsAdminTest(ArmContentTestCase):
    fixtures = ['admin.json', ]

    def test_authors_fields_are_listed_as_such(self):
        self.client.login(username="admin", password="admin")
        url = reverse("admin:arm_content_support_simpleauthoredmodel_add")
        response = self.client.get(url)
        label_pattern = r'<label [^>]*for="id_authors"[^>]*>Authors:</label>'
        self.assertRegexpMatches(str(response), label_pattern)

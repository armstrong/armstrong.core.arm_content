from django.contrib.auth.models import User
from django.test import TestCase

from .models import SimpleProfile


class SimpleProfileTestCase(TestCase):
    def test_get_absolute_url_slugifies_users_name(self):
        user = User.objects.create(username="travis", first_name="Travis",
                last_name="Swicegood")
        profile = SimpleProfile(user=user)
        self.assertEqual("/travis-swicegood/", profile.get_absolute_url())

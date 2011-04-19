from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


def user_to_link(user):
    try:
        return '<a href="%s">%s</a>' % (user.get_profile().get_absolute_url(), user.get_full_name())
    except ObjectDoesNotExist:
        return user_to_name(user)


def user_to_name(user):
    return user.get_full_name()


class Authors(models.Model):
    users = models.ManyToManyField(User)
    override = models.CharField(max_length=200)
    extra = models.CharField(max_length=200)

    def __unicode__(self, formatter=user_to_name):
        if self.override:
            return self.override
        names = [formatter(a) for a in self.users.all()]
        ret = u', '.join(names[:-2] + \
                [(u', ' if self.extra else u' and ').join(names[-2:])])
        if self.extra:
            space = ' ' if self.extra[0].isalpha() else ''
            ret = u"%s%s%s" % (ret, space, self.extra)
        return ret

    def html(self):
        return self.__unicode__(formatter=user_to_link)

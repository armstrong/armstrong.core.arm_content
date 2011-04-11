from django.contrib.auth.models import User
from django.db import models


class Authors(models.Model):
    users = models.ManyToManyField(User)
    override = models.CharField(max_length=200)
    extra = models.CharField(max_length=200)

    def __unicode__(self):
        if self.override:
            return self.override
        names = [a.get_full_name() for a in self.users.all()]
        ret = ', '.join(names[:-2] + [' and '.join(names[-2:])])
        if self.extra:
            ret = "%s %s" % (ret, self.extra)
        return ret

Publications
============
Armstrong supplies two mixins for storing information on your model that
explains its publication status.  These are used by default in the various
``armstrong.apps`` components that expose models that can be published.


Mixins
------
All mixins are declared as `abstract models`_.  For more information on
Armstrong's use of mixins, see Armstrong Mixins.

.. todo:: Cross reference the yet-to-be-written Armstrong Mixins section.

.. _abstract models: https://docs.djangoproject.com/en/1.3/topics/db/models/#abstract-base-classes

``SimplePublicationMixin``
""""""""""""""""""""""""""
This provides what Armstrong deems as the minimum amount of information needed
to determine the publication status.  It contains two fields::

    pub_date = models.DateTimeField(db_index=True)
    pub_status = models.CharField((u'Publication status'), max_length=1,
        choices=PUB_STATUS_CHOICES, help_text=(
            u'Only published items will appear on the site'))

The two constants used in ``pub_status`` are defined as::

    PUB_STATUS_CHOICES = (
        ('D', 'Draft'),
        ('E', 'Edit'),
        ('P', 'Published'),
        ('T', 'Trash'),
    )

    PUB_STATUSES = dict((pair[1], pair[0]) for pair in PUB_STATUS_CHOICES)

You can use this mixin in your model like this::

    from armstrong.core.arm_content import mixins
    from django.db import models

    class MyArticle(mixins.SimplePublicationMixin, models.Model):
        # your custom fields here

Note the order of the parent classes.  ``models.Model`` needs to come last in
the list so Django can properly identify your object as a model.

``PublicationMixin``
""""""""""""""""""""
This is an extension of the ``SimplePublicationMixin`` mixin and provides a
``sites`` field like this::

    sites = models.ManyToManyField(Site)

You add it to your custom models the same way you do
``SimplePublicationMixin``.

::

    from armstrong.core.arm_content import mixins
    from django.db import models

    class MyArticle(mixins.SimplePublicationMixin, models.Model):
        # your custom fields here


.. note:: There are plans to introduce a new ``Publication`` model that
          works similar to ``django.contrib.sites``, but allows for multiple
          "publications" on each site.  Once that is added, it will be added to
          the ``PublicationMixin``.

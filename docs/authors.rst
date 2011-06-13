Authors
=======

Armstrong provides you with a custom ``AuthorsField`` field for managing
authors of a given model.  It allows you to link multiple users to a model and
deal with generating a byline for that model.


AuthorField Usage
-----------------

You can add it to any model the way you would any other field in Django::

    from armstrong.core.arm_content.fields import AuthorsField
    from django.db import models

    class MyArticle(models.Model):
        authors = AuthorsField()
        # the rest of your model...

By default, ``AuthorsField`` assumes you want to connect to the ``User`` model
in ``django.contrib.auth``.  You can provide your own custom user model by
providing a model class when you declare the field like this::

    from armstrong.core.arm_content.fields import AuthorsField
    from django.db import models
    from myapp.models import CustomUser

    class MyArticle(models.Model):
        authors = AuthorsField(CustomUser)
        # the rest of your model...

Once you have an authors field, you can display a list of all of the users by
casting the field to a string.

::

    articles = MyArticle.objects.create()
    articles.authors.add(bob)
    articles.authors.add(alice)
    print "%s" % articles.authors
    # outputs "Bob Example, and Alice Example"

You can create an HTML representation of your model by printing the ``.html``
attribute on the ``authors`` field like this::

    print "%s" % articles.authors.html()

This returns a string with links to the profile for each user as determined by
calling the user's ``get_profile().get_absolute_url()``.  It returns a
plain-text name for any users that do not have a profile.

Both casting to a string and converting to HTML take into consider any extra
information or overrides that are configured for the given ``AuthorsField``.


Adding Additional Info to the Byline
""""""""""""""""""""""""""""""""""""
Sometimes you need to supply additional information to be used in the byline.
By default, the ``AuthorsField`` looks for an ``authors_extra`` field on the
model instance.  Anything you provide here is appended to the end of the known
users.

For example, if your model looked like this::

    from armstrong.core.arm_content.fields import AuthorsField
    from django.db import models

    class MyArticle(models.Model):
        authors = AuthorsField()
        authors_extra = models.CharField(max_length=100)

Then your instance would look like this::

    article = MyArticle.objects.create(authors_extra=", and everyone else")
    article.authors = [bob, alice]

    print "%s" % article.authors
    # outputs "Bob Example, Alice Example, and everyone else"

Note that there is no space between the "``,``" and the last name of a user.
``AuthorsField`` is smart enough to do the right thing depending on the first
character.  For example::

    article = MyArticle.objects.create(authors_extra="and everyone else")
    article.authors = [bob, alice]

    print "%s" % article.authors
    # outputs "Bob Example, Alice Example and everyone else"

If the first character is a letter (passes ``str.isalpha()``), a space is added
between the last name and the extra information.  It assumes that anything else
is meant to be joined directly to the list, like the case of our earlier
example that begins with a comma.

Customizing the name of the extra field
'''''''''''''''''''''''''''''''''''''''
You can provide a custom field name for the ``AuthorsField`` instead of the
default ``authors_extra`` field.  To set it, provide a string that represents
the field name to ``extra_field_name`` like this::

    class MyArticle(models.Model):
        authors = AuthorsField(extra_field_name="custom_extra")
        custom_extra = models.CharField(max_length=100)


Overriding the Byline
"""""""""""""""""""""
You can also override the byline entirely with the ``authors_override`` field.
If that field is present on a model and is not empty, it will be used in place
of what would normally be generated.  Consider a model that looks like this::

    from armstrong.core.arm_content.fields import AuthorsField
    from django.db import models

    class MyArticle(models.Model):
        authors = AuthorsField()
        authors_override = models.CharField(max_length=100)

This behaves like this::

    article = MyArticle.objects.create(authors_override="Custom byline")
    article.authors = [bob, alice]

    print "%s" % article.authors
    # outputs "Custom byline"

Customizing the name of the override field
''''''''''''''''''''''''''''''''''''''''''
You can change the override field name for an ``AuthorsField`` by providing
the ``override_field_name`` keyward argument like this::

    class MyArticle(models.Model):
        authors = AuthorsField(override_field_name="custom_override")
        custom_override = models.CharField(max_length=100)


AuthorsMixin Usage
------------------
Armstrong uses mixins for grouping several fields together into a common,
reusable object.  The ``AuthorsMixin`` allows you to add the default behavior
of an authored model in Armstrong to your model.  You can mix it into your
models like this::

    from armstrong.core.arm_content.mixins import AuthorsMixin
    from django.db import models

    class MyArticle(AuthorsMixin, models.Model):
        # Your fields here...

Using this adds the ``authors``, ``authors_extra``, and ``authors_override``
fields to your model.

.. important::
    Note parent object order.  You *must* declare the ``models.Model`` class as
    the last class in the list of parent classes.


Admin Helpers
-------------
To keep things consistent inside Armstrong, we use the same fieldsets
throughout the admin.  Use the ``armstrong.core.arm_content.fieldsets.AUTHORS``
variable to add the default author's fieldset to your models.

Your ``ModelAdmin`` should look similar to this::

    from armstrong.core.arm_content import fieldsets
    from django.contrib import admin

    class MyArticleAdmin(admin.ModelAdmin):
        fieldsets = (
            # your main fields here like this:
            (None, {
                "fields": ("title", "body", )
            }),

            fieldsets.AUTHORS,
        )

This is the same as adding the following to your ``fieldsets`` tuple::

    ('Author Information', {
        'fields': ('authors', 'authors_override', 'authors_extra'),
    })

.. warning::
    This is not currently internationalized

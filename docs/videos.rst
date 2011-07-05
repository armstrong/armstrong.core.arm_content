Embedded Videos
===============
Armstrong provides a custom field for dealing with embedded videos.  That is,
videos that are hosted elsewhere.  You can add your own backends (see `Creating
Custom Backends`_), or use the default ones that are included: Vimeo or
YouTube.


Configuring Embedded Videos
---------------------------
There are three settings that need to be set for you to use embedded video
fields or mixins:

``ARMSTRONG_EXTERNAL_VIDEO_BACKEND``
    Each ``EmbeddedVideo`` (the actual representation of an ``EmbeddedVideoField``)
    has a backend that parsed it and can handle turning the raw URL into an
    embedded form.  Armstrong comes with two backends by default, the
    ``VimeoBackend`` and ``YouTubeBackend`` located in the
    ``armstrong.core.arm_content.video.backends`` module.

    You can configure one or more backends by adding the
    ``ARMSTRONG_EXTERNAL_VIDEO_BACKEND`` settings.  To set one backend, use a
    string::

        ARMSTRONG_EXTERNAL_VIDEO_BACKEND = "armstrong.core.arm_content.video.backend.VimeoBackend"

    You can configure multiple backends by changing it to an iterable like this::

        ARMSTRONG_EXTERNAL_VIDEO_BACKEND = [
            "armstrong.core.arm_content.video.backend.VimeoBackend",
            "armstrong.core.arm_content.video.backend.YouTubeBackend",
        ]

.. warning:: ``ARMSTRONG_EXTERNAL_VIDEO_BACKEND`` must be configured as of
             v0.3.x.  This is going to change in a future version.

.. todo:: Update docs once `14622611`_ has been completed.
.. _14622611: https://www.pivotaltracker.com/story/show/14622611

``ARMSTRONG_EMBED_VIDEO_WIDTH`` and ``ARMSTRONG_EMBED_VIDEO_HEIGHT``
    Many sites display all videos at a particular width and height.  Setting
    these values allows you specify those default values without having to pass
    ``width`` and ``height`` kwargs to ``embed`` on every call (see below).

Using the Field
---------------
Use ``EmbeddedVideoField`` to store URLs that can be presented as an embeddable
video.  ``EmbeddedVideoField`` is a subclass of Django's built-in ``URLField``,
so all of the validation that occurs on that field is performed as well.

You can add it to your model like any other field.

::

    from armstrong.core.arm_content import fields
    from django.db import models

    class Video(models.Model):
        video = fields.EmbeddedVideoField()

You can access the embedded representation of the field via its ``embed``
method like this::

    v = Video.objects.create(url="http://www.youtube.com/watch?v=QwIphm5wVAs")
    html_code = v.embed()

``html_code`` is now a string that looks like this (but without the ``\n`` that
are included here for ease of reading) if you have a configured default
width and height of ``480`` and ``270``, respectively::

        <iframe title="YouTube video player" width="480" height="270"
            src="http://www.youtube.com/embed/QwIphm5wVAs"
            frameborder="0" allowfullscreen></iframe>

You can specify the width and height of videos by providing a ``width`` and
``height`` kwarg, respectively.  Both the Vimeo and YouTube backends provided
by Armstrong support this kwarg.  See `Configuring Embedded Videos`_ for
more information about what backends are provided and what they support.


Using the Mixin
---------------
Armstrong also provides an ``EmbeddedVideoMixin`` if you prefer that style of
declaration rather than explicitly adding the fields to your model.  You can
add it like this::

    from armstrong.core.arm_content import mixins
    from django.db import models

    class Video(mixins.EmbeddedVideoMixin, models.Model):
        # your custom fields here

This adds a field called ``video`` to your model.  Like all Armstrong mixin,
make sure ``models.Model`` is the last class listed to ensure Django can
recognize your model as a real model.


Creating Custom Backends
------------------------
You can add your own backends by creating an object that provides two methods:
``prepare(video)`` and ``embed(**kwargs)``.

``prepare(video)``
    This is called by ``EmbeddedVideo`` when it is instantiated.  It receives
    the ``EmbeddedVideo`` instance that called it.  It should return ``True``
    if was able to work, otherwise it should return ``None``.  It should also
    be fault-tolerant.  It may get things that it URLs that it doesn't know
    how to handle.  It shouldn't raise any exceptions as other backends may
    know how to deal with the provided video URL.

``embed(width=None, height=None)``
    Embed is responsible for returning a chunk of HTML that can be used for
    displaying the embedded version of the URL.  Embed can utilize as many
    ``kwargs`` as it likes but must take a ``width`` and ``height`` keyword
    argument.  Any kwargs passed ``EmbeddedVideo.embed`` are passed through to
    the backend.  It is currently the job of the backend to be able to handle
    what is passed to it, so adding a ``**kwargs`` to your backend is
    suggested.

    The ``armstrong.core.arm_content.video.backends.helpers.inject_defaults``
    decorator determines the default ``width`` and ``height`` and adds them as
    kwargs for you.  It's recommended that you decorate all of your backends
    with this so default width and heights are used.

.. warning:: Your custom backends must be capable of gracefully handling
             anything thrown at them.  ``prepare`` may encounter a video that
             it can't parse and ``embed`` might get extra ``kwargs`` that it
             doesn't use.

             You need to handle these instances yourself, for now.  Once
             `14628217`_ is implemented, backends can be simplified because
             the fault-tolerance will be moved further up the stack.  Tread
             carefully for now.

.. _14628217: https://www.pivotaltracker.com/story/show/14628217
.. todo:: Update docs here once the code has changed

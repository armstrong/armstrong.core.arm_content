Audio Field
===============
Armstrong provides a custom field for dealing with Audio Files. You can 
add your own backends (see `Creating Custom Backends`_), or use one that
has already been written: mutagen or id3reader


Configuring Audio Field 
---------------------------
There are three settings that need to be set for you to use the audio 
field to access audio metadata such as artist or track number.

``ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND``
    Each ``AudioFile`` (the actual representation of an ``AudioFileField``)
    has a backend that parses the tags in the audio file.  Armstrong provides 
    two backends, ``armstrong.core.arm_content.audio.Id3readerBackend`` and 
    ``armstrong.apps.audio.backends.mutagen.MutagenBackend``

    You can configure one or more backends by adding the
    ``ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND`` settings.  To set one backend, use a
    string::

        ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND = "armstrong.apps.audio.backends.mutagen"

.. warning:: ``ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND`` must be configured as of
                v0.3.x.  This may change in a future version.

Using the Field
---------------
Use the ``AudioFileField`` when you want to provide more specialized audio 
functionality at the django layer.  ``AudioFileField`` is a subclass of 
``FileField``, and uses the same database representation to hold the filename
so if your already using ``FileField`` to store your audio files, you shouldn't 
have to change database repersentation of your model to switch to the 
``AudioFileField``.


The ``AudioFileField`` will look at the model that it is attached to and prepopulate any field 
that shares a name with a piece of extracted metadata. For instance if the model 
has a artist field and is empty, then the audiofield will pre populate it with 
the data contained in the artist tag contained in the uploaded file

You can add it to your model like any other field.

::

    from armstrong.core.arm_content import fields
    from django.db import models

    class Audio(models.Model):
        audio_file = fields.AudioFileField()
        #optional fields that audio will pre populate
        artist = models.CharField(max_length=100)
        genre = models.CharField(max_length=100)
        album = models.CharField(max_length=100)
        title = models.CharField(max_length=100)
        comment =  models.CharField(max_length=100) 

You can also call the metadata fields whatever you want 

::

    from armstrong.core.arm_content import fields
    from django.db import models

    class Audio(models.Model):
        audio_file = fields.AudioFileField(artist_field_name='foo',
                                           genre_field_name='bar',
                                           album_field_name='baz',
                                           title_field_name='qrs',
                                           comment_field_name='tkc')
        #optional fields that audio will pre populate
        foo = models.CharField(max_length=100)
        bar = models.CharField(max_length=100)
        baz = models.CharField(max_length=100)
        qrs = models.CharField(max_length=100)
        tkc =  models.CharField(max_length=100) 

You can expose the audio file as a player via:

::

    a = Audio(audio_file='test.mp3') 
    print a.html

``a.html`` is now a string that looks roughly like this.::
    <script type="text/javascript">
    (function($){
        $(document).ready(function(){
            $("#af_player_6").jPlayer({
                ready: function () {
                    $(this).jPlayer("setMedia", {
                        mp3: "test.mp3"
                    });
                },
                solution: "html, flash",
                swfPath: "/static/js",
                cssSelectorAncestor: "#jp_interface_6",
                supplied: "mp3"
             }).jPlayer("load")
               .bind($.jPlayer.event.play, function() { 
                    // Using a jPlayer event to avoid both jPlayers playing together.
                    $(this).jPlayer("pauseOthers");
             });
        });
    })(jQuery || django.jQuery);
    </script>
    <div class="jp-audio">
        <div class="jp-type-single">
            <div id="af_player_6" class="jp-jplayer"></div>
            <div id="jp_interface_6" class="jp-interface">
                <ul class="jp-controls">
                    <li><a href="#" class="jp-play" tabindex="1">play</a></li>
                    <li><a href="#" class="jp-pause" tabindex="1">pause</a></li>
                    <li><a href="#" class="jp-stop" tabindex="1">stop</a></li>
                    <li><a href="#" class="jp-mute" tabindex="1">mute</a></li>
                    <li><a href="#" class="jp-unmute" tabindex="1">unmute</a></li>
                </ul>
                <div class="jp-progress">
                    <div class="jp-seek-bar">
                        <div class="jp-play-bar"></div>
                    </div>
                </div>
                <div class="jp-volume-bar">
                    <div class="jp-volume-bar-value"></div>
                </div>
                <div class="jp-current-time"></div>
                <div class="jp-duration"></div>
            </div>
            <div id="jp_playlist_6" class="jp-playlist">
                <ul>
                    <li>test audio file</li>
                </ul>
            </div>

        </div>
    </div>

This code can be divided into two parts, javascript, which is the actual invocation of the player, and the html that makes up the gui of the player.  At the end of the javascript section you may notice ``(jQuery || django.jQuery)``, which is basically a way to allow the same javascript to work inside the admin, which djangos version of jQuery, or in a template with jQuery in the usual place. The important values to note are the url ``test.mp3``, which is the file url, ``/static/`` which is the static file prefix, ``mp3`` which is the file type.

.. warning:: if you use the audiomodel.html in a template YOU MUST INCLUDE JQUERY AND JPLAYER. 

What you would do to include js files required would look something like:

::
    {% load static %}
    {% get_static_prefix as STATIC_PREFIX %}

    <html>
    <head>
    <title>audio lists</title>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" ></script>
    <script type="text/javascript" src="{{STATIC_PREFIX}}js/jquery.jplayer.min.js"> </script>
    <link href="{{STATIC_PREFIX}}skin/jplayer.blue.monday.css" rel="stylesheet" type="text/css" />

    </head>

The player will also be used as part of a form if the ``AudioField`` of the form has allready been filled in and uploaded.


Using the Audio Mixin
------------------------
The audio mixin just makes it easier to include the standard audio metadata fields in your model. Instead of the first Audio model above, which is long and convoluted, you can just write::
    from armstrong.core.arm_content import mixins
    class Audio(mixins.AudioMixin): pass


Creating Custom Backends
------------------------
You can add your own backends by creating an object with the following methods.

::

    def filetype(file);
    """
        returns a string decalring the file type
    """
    
    def metadata(file):
    """
        returns a dictionary full of ["tagname"]="value"  pairs
    """



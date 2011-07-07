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

you can expose the audio file as a player via:

::

    a=Audio(audio_file='test.mp3') 
    html_code=a.render()

``html_code`` is now a string that looks like this, without the comments.::

    <div id="%(playerdivid)" class="jp-jplayer"></div>
        <script type="text/javascript">
        //<![CDATA[
        //if jquery is included allready, we dont need load it again 
        if (!window.jQuery){
            document.write('<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" />')
        }
        //if jplayer is included allready, we dont need load it again
        if (!window.jQuery.jPlayer){
            document.write('<script type="text/javascript" src="/static/js/jplayer.js" />')
        }
        $(document).ready(function(){
            $("#jquery_jplayer_1").jPlayer({
                ready: function () {
                    $(this).jPlayer("setMedia", {
                        mp3: "/static/audio/test.mp3"
                    },
                swfPath: "../js",
                supplied: "mp3"
                }).jPlayer("load");   
            });
        });
        //]]>

This code can be devided into tiwo parts, one part right below //<!CDATA[, which is the conditiontal include of the jplayer.js file, and the actual invocation of the player itself.  The important values to note are the url ``/static/audio/test.mp3``, which is the file url, ``/static/`` which is the static file prefix, ``mp3`` which is the file type.


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



from django.db.models.fields import FileField, FieldFile
from django.core.files import File
from amrstrong.core.arm_content.widgets import AudioFileWidget

class AudioField(FileField):
    attr_class=AudioFile
    def __init__(self, verbose_name=None, name=None, **kwargs):
        FileField.__init__(self, verbose_name, name, **kwargs)

    def contribute_to_class(self, cls, name):
        super(AudioField, self).contribute_to_class(cls, name)
        # Attach update_playtime_field so that dimension fields declared
        # after their corresponding image field don't stay cleared by
        # Model.__init__, see bug #11196.
        signals.post_init.connect(self.update_metadata, sender=cls)

    def update_metadata():
        """
        may not need to exist, we shall see
        """
        pass 
        
    def formfield(self, **kwargs):
        defaults = {'widget': AudioFileWidget}
        defaults.update(kwargs)
        return super(AudioField, self).formfield(**defaults)

class AudioFile(FieldFile):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with audio files.
    """
    
    def __init__(self, *args, **kwargs):
        super(AudioFile,self).__init__(self, *args, **kwargs)

    def _transcode(self, toformat):
        """
        returns a transcoded file 
        perhaps should do more complex and diffrent things
        like transcode via zencoder
        """
        pass

    def _get_format(self):
        """
        get the encoding of the file 
        """
        if not hasattr(self, 'audioformat'):
            pass
        return self.audioformat

    def _get_playtime(self):
        """
        get the playtime of the file 
        """
        pass

    def _get_bitrate():
        """
        get the bit rate 
        """
        pass

    def _get_metadata_dict():
        """
        get the all metadata as a dictionary 
        """
        pass

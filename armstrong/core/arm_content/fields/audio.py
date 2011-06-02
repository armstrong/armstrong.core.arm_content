from django.db.models import signals
from django.db.models.fields.files import FileField, FieldFile, FileDescriptor

from armstrong.core.arm_content.fields.widgets import AudioFileWidget


class AudioFile(FieldFile):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with audio files.
    """
    
    def __init__(self, *args, **kwargs):
        super(AudioFile,self).__init__( *args, **kwargs)
        if 'metadata' in kwargs:
            self._metadata= kwargs['metadata']

    def _transcode(self, toformat):
        """
        returns a transcoded file 
        perhaps should do more complex and diffrent things
        like transcode via zencoder
        """
        raise NotImplementedError

    @property
    def filetype(self):
        """
        get the encoding of the file 
        """
        raise NotImplementedError

    @property
    def playtime(self):
        """
        get the playtime of the file 
        """
        raise NotImplementedError

    @property
    def bitrate(self):
        """
        get the bit rate 
        """
        raise NotImplementedError

    @property
    def metadata(self):
        """
        get the all metadata as a dictionary 
        """
        from  mutagen import File as MutagenFile
        if not hasattr(self,'_metadata'):
            self._metadata=MutagenFile(self, easy=True)
        return self._metadata


class AudioFileDescriptor(FileDescriptor):
    """
    Just like the FileDescriptor, but for AudioFields. The only difference is
    assigning the audio metadata to the metadata dict, if appropriate.
    """
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super(AudioFileDescriptor, self).__set__(instance, value)
        if previous_file is not None:
            self.field.update_metadata(instance, force=True)


class AudioField(FileField):
    attr_class=AudioFile
    descriptor_class=AudioFileDescriptor
    
    def contribute_to_class(self, cls, name):
        super(AudioField, self).contribute_to_class( cls, name)
        # Attach update_playtime_field so that dimension fields declared
        # after their corresponding image field don't stay cleared by
        # Model.__init__, see bug #11196.
        signals.post_init.connect(self.update_metadata, sender=cls)

    def update_metadata(self, instance, force=False, *args, **kwargs):
        """
        may not need to exist, we shall see
        """
        pass
        #metadata={'test':'test'}
        #setattr(instance, 'metadata', metadata)
        #self.metadata=metadata

    def formfield(self, **kwargs):
        defaults = {'widget': AudioFileWidget}
        defaults.update(kwargs)
        return super(AudioField, self).formfield(**defaults)

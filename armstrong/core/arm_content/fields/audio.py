from django.db.models import signals
from django.db.models.fields.files import FileField, FieldFile, FileDescriptor

from armstrong.core.arm_content.fields.widgets import AudioFileWidget
from armstrong.utils.backends import GenericBackend 

from django.conf import settings


class AudioFile(FieldFile):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with audio files.
    """
    
    def __init__(self, *args, **kwargs):
        super(AudioFile,self).__init__( *args, **kwargs)
        if 'metadata' in kwargs:
            self._metadata= kwargs['metadata']
        backendKlass=GenericBackend('ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND').get_backend()
        #get a instance of said class with the file set
        self.backend=backendKlass


    def _transcode(self, toformat):
        """
        returns a transcoded file 
        perhaps should do more complex and diffrent things
        like transcode via zencoder
        """
        raise NotImplementedError

    def render(self,*args, **kwargs):
        if('armstrong.apps.audio' in settings.INSTALLED_APPS):
            from armstrong.apps.audio import widget
            return widget.render(self, args, kwargs)
        else:
            return "<a href='%s'> %s </a>" % (self.url, self.name)

    @property
    def filetype(self):
        """
        get the encoding of the file 
        """
        if not hasattr(self,'_filetype'):
            self._filetype = self.backend.filetype(self.file)
        return self._filetype

    @property
    def playtime(self):
        """
        get the playtime of the file 
        """
        if not hasattr(self,'_playtime'):
            self._playtime = self.backend.playtime(self.file)
        return self._playtime

    @property
    def bitrate(self):
        """
        get the bit rate 
        """
        if not hasattr(self,'_bitrate'):
            self._bitrate = self.backend.bitrate(self.file)
        return self._bitrate

    @property
    def metadata(self):
        """
        get the all metadata as a dictionary 
        """
        if not hasattr(self,'_metadata'):
            self._metadata= self.backend.metadata(self.file)
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

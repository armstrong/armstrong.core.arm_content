from django.db.models import signals
from django.db.models.fields.files import FileField, FieldFile, FileDescriptor
from django.forms.fields import FileField as FileFormField
from django.template.loader import get_template
from django.template import Context

from armstrong.core.arm_content.fields.widgets import AudioFileWidget
from armstrong.utils.backends import GenericBackend


class AudioFile(FieldFile):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with audio files.
    """

    def __init__(self, *args, **kwargs):
        super(AudioFile, self).__init__(*args, **kwargs)
        #allows the override of anything that follows the _attrname caching pattern
        for attr in dir(self):
            if attr in kwargs:
                setattr(self, '_' + attr, kwargs[attr])
        self.backend = \
            GenericBackend('ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND')\
            .get_backend()

    def _transcode(self, toformat):
        """
        returns a transcoded file
        perhaps should do more complex and different things
        like transcode via zencoder
        """
        raise NotImplementedError

    def render(self, *args, **kwargs):
        audio_player_template = get_template('audio/player.html')
        return audio_player_template.render(
                            Context(
                                {'url': self.url,
                                'filetype': self.filetype,
                                'name': self.metadata['title'],
                                'fileno': str(self.fileno())
                                }
                            )
                        )

    @property
    def filetype(self):
        """
        get the encoding of the file
        """
        if not hasattr(self, '_filetype'):
            self._filetype = self.backend.filetype(self.file)
        return self._filetype

    @property
    def playtime(self):
        """
        get the playtime of the file
        """
        if not hasattr(self, '_playtime'):
            self._playtime = self.backend.playtime(self.file)
        return self._playtime

    @property
    def bitrate(self):
        """
        get the bit rate
        """
        if not hasattr(self, '_bitrate'):
            self._bitrate = self.backend.bitrate(self.file)
        return self._bitrate

    @property
    def metadata(self):
        """
        get the all metadata as a dictionary
        """
        if not hasattr(self, '_metadata'):
            self._metadata = self.backend.metadata(self.file)
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
            self.field.update_metadata(instance, )


class AudioFormField(FileFormField):
    widget = AudioFileWidget


class AudioField(FileField):
    attr_class = AudioFile
    descriptor_class = AudioFileDescriptor

    def __init__(self, *args, **kwargs):
        self.overrides = {}
        for key in kwargs.keys():
            if key.endswith('_field_name'):
                self.overrides[key] = kwargs[key]
                del(kwargs[key])
        return super(AudioField, self).__init__(self, *args, **kwargs)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def contribute_to_class(self, cls, name):
        super(AudioField, self).contribute_to_class(cls, name)
        # Attach update_metadata so that dimension fields declared
        # after their corresponding image field don't stay cleared by
        # Model.__init__, see bug #11196.
        signals.post_init.connect(self.update_metadata, sender=cls)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': AudioFormField}
        defaults.update(kwargs)
        return super(FileField, self).formfield(**defaults)

    def update_metadata(self, instance, *args, **kwargs):
        """
        update the metadata  IF a file has been set
        instance == the model

        """
        audio_file = getattr(instance, self.name)
        if hasattr(audio_file, "file"):
            for key in audio_file.metadata.keys():
                field_name = self.overrides.get(key + '_field_name', key)
                if not (hasattr(instance, field_name) and  getattr(instance, field_name)):
                    setattr(instance, field_name, audio_file.metadata[key])

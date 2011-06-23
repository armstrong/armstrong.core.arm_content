from django.core.exceptions import ImproperlyConfigured


class MutagenBackend(backend):
    def __init__(self, file):
        self.file=file

    def filetype(self):
        return self.mute.mime[0].replace('audio/','')

    @property
    def metadata(self):
        """ converts the metada to a nice neat dictionary"""
        try:
            from  mutagen import File as MutagenFile
            self.mute=MutagenFile(self, easy=True)
            return dict(mutagen)
        except ImportError:
            msg = "Unable to find 'mutagen' backend, " \
                "please make sure it is installed or "\
                "via pip install -e git://github.com/Jbonnett/Mutagen-flo.git#egg=mutagen"\
                "use the id3reader backend"
            raise ImproperlyConfigured(msg)


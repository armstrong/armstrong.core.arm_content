from django.core.exceptions import ImproperlyConfigured

from armstrong.core.arm_content.audio import AudioBackend 

FT_TRANSLATIONS={
    'vorbis':'oga',
    
    }
class MutagenBackend(AudioBackend):
    def filetype(self, file):
        
        ftype=self.load(file).mime[0].replace('audio/','')
        return FT_TRANSLATIONS[ftype] if ftype in FT_TRANSLATIONS.keys() else ftype


    def load(self, file):
        """ converts the metada to a nice neat dictionary"""
        try:
            from  mutagen import File as MutagenFile
            mute=MutagenFile(file, easy=True)
            return (mute)
            
        except ImportError:
            msg = "Unable to find 'mutagen' backend, " \
                "please make sure it is installed or "\
                "via pip install -e git://github.com/Jbonnett/Mutagen-flo.git#egg=mutagen"\
                "use the id3reader backend"
            raise ImproperlyConfigured(msg)

    def metadata(self, file):
        return dict(self.load(file))

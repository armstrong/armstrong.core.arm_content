
import pkg_resources
pkg_resources.declare_namespace(__name__)

AUDIO_BACKEND_SETTING='ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND'

class AudioBackend(object): 
    def __init__(self, file):
        self.file

    @property
    def filetype(self):
        raise NotImplementedError

    @property
    def metadata(self):
        raise NotImplementedError
    
    @property
    def playtime(self):
        raise NotImplementedError

    @property
    def bitrate(self):
        raise NotImplementedError

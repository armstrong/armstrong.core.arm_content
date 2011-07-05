import pkg_resources
pkg_resources.declare_namespace(__name__)

AUDIO_BACKEND_SETTING='ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND'

class AudioBackend: 
    def filetype(self, file):
        raise NotImplementedError

    def metadata(self, file):
        raise NotImplementedError
    
    def playtime(self, file):
        raise NotImplementedError

    def bitrate(self, file):
        raise NotImplementedError

from id3proxy import Id3readerBackend

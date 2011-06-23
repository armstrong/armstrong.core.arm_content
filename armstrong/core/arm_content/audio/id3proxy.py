#wrapper for the id3reader.py
import id3reader

class Id3readerBackend:
    """wrapper for the "don't make me regret this licensed"  id3 reader written by Ned Batchelder"""
    def __init__(self, file):
       self.file=file

    @poperty
    def filetype(self):
        if self.file.name.lower().rfind('.mp3') == len(self.file.name)-3):
            return 'mp3'
        else:
            return 'unsupported'

    @property
    def metadata(self):
        """ converts the metada to a nice neat dictionary"""
        reader=id3reader.Reader(self.file)
        metadata=dict()
        for fr in reader.allframes:
            if hasattr(fr, 'value'):
                metadata[fr.id] = fr.value
        print metadata
        return metadata

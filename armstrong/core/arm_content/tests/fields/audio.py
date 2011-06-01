# coding=utf-8
from django.contrib.auth.models import User
from django.db import models

from ..arm_content_support.models import AudioModel
from ..arm_content_support.forms import AudioModelForm
from ..arm_content_support.models import SimpleProfile
from .._utils import *

from ...fields import AudioField
from ...fields.widgets.audio import AudioFileWidget 

class AudioFieldMetadataTestCase(TestCase):
    def setUp(self):
        if type(self) is AudioFieldMetadataTestCase:
            return self.skipTest('parrent class')
        self.audiofile = load_audio_file(self.audio_metadata['filename'])

    def test_audiofield_default_widget(self):
        """
        test that the correct widget is displayed in 
        a model form 
        """
        form=AudioModelForm()
        self.assertTrue(type(form.fields['audio_file'].widget) is AudioFileWidget)
   
    def test_audiofield_metadata(self):
        """
        confirm that the extracted metadata matches the expected values 
        """
        print self.audio_metadata
        print 'vs'
        print self.audiofile.audio_file.metadata
        for key in self.audio_metadata.keys():
            self.assertEqual(self.audio_metadata[key], self.audiofile.audio_file.metadata[key])


class Mp3Test(AudioFieldMetadataTestCase):
    """
    tests the audio fiels support for mp3's
    """
    filename='test.mp3'


    audio_metadata={'album': [u'Quod Libet Test Data'], 'title': [u'Silence'], 'artist': [u'piman'], 'genre': [u'Darkwave'], 'date': [u'2004'], 'tracknumber': [u'2']}


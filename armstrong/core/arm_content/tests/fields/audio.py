# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from ..arm_content_support.models import AudioModel, OverrideAudioModel
from ..arm_content_support.forms import AudioModelForm
from ..arm_content_support.models import SimpleProfile

from .._utils import *
from ...fields import AudioField
from ...fields.widgets.audio import AudioFileWidget


class AudioFieldMetadataTestCase(ArmContentTestCase):
    def setUp(self):
        if type(self) is AudioFieldMetadataTestCase:
            return self.skipTest('parrent class')
        self.audio_model = load_audio_model(self.filename)
        self.override_audio_model =\
            load_audio_model(self.filename, model=OverrideAudioModel)

    def test_audiofield_default_widget(self):
        """
        test that the correct widget is displayed in
        a model form
        """
        form = AudioModelForm()
        self.assertTrue(
            type(form.fields['audio_file'].widget) is
            AudioFileWidget)
        import pdb;pdb.set_trace()
        form2 = AudioModelForm(initial={
                               "audio_file": self.audio_model.audio_file})
        self.assertTrue(self.audio_model.audio_file.url in form2.as_ul())
        self.assertTrue("jplayer.js" in form2.as_ul())
                

    def test_audiofield_filetype(self):
        """
        test that the file type returned by the file field is correct
        """
        self.assertEqual(self.audio_model.audio_file.filetype, self.filetype)

    def test_audiofield_metadata(self):
        """
        confirm that the extracted metadata matches the expected values
        """
        for key in self.audio_metadata.keys():
            self.assertEqual(
                    self.audio_metadata[key],
                    self.audio_model.audio_file.metadata[key])

    def test_audio_model_overriding(self):
            '''test the audio model field pre population'''
            self.override_audio_model.save()
            unoverridden = OverrideAudioModel.objects.get(
                                        pk=self.override_audio_model.pk)

            self.assertEqual(self.audio_metadata['artist'], unoverridden.artist)
            self.override_audio_model.artist = 'qr'
            self.override_audio_model.save()

            overridden = OverrideAudioModel.objects.get(pk=self.override_audio_model.pk)

            self.assertEqual('qr', overridden.artist)


class Id3readerTest(AudioFieldMetadataTestCase):
    """
    test id3reader
    """
    filename = 'test.mp3'
    filetype = 'mp3'
    playtime = '4'
    audio_metadata = {'album': u'Quod Libet Test Data',
                     'title': u'Silence',
                     'artist': u'piman',
                     'genre': u'Darkwave',
                     'date': u'2004',
                     'tracknumber': u'2'}


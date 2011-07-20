# coding=utf-8
from django.conf import settings

from ..arm_content_support.models import OverrideAudioModel
from ..arm_content_support.forms import AudioModelForm

from .._utils import *
from ...fields.widgets.audio import AudioFileWidget

__all__ = ["Mp3Test"]

class AudioFieldMetadataTestCase(ArmContentTestCase):
    def setUp(self):
        self.audio_model = load_audio_model(self.filename)
        self.override_audio_model = load_audio_model(self.filename,
                model=OverrideAudioModel)

    def test_audiofield_default_widget(self):
        """
        test that the correct widget is displayed in
        a model form
        """
        form = AudioModelForm()
        self.assertTrue(
            type(form.fields['file'].widget) is
            AudioFileWidget)
        form2 = AudioModelForm(initial={
                               "file": self.audio_model.file})
        self.assertTrue(self.audio_model.file.url in form2.as_ul())
        self.assertTrue("jplayer" in form2.as_ul())
                

    def test_audiofield_filetype(self):
        """
        test that the file type returned by the file field is correct
        """
        self.assertEqual(self.audio_model.file.filetype, self.filetype)

    def test_audiofield_metadata(self):
        """
        confirm that the extracted metadata matches the expected values
        """
        for key in self.audio_metadata.keys():
            self.assertEqual(
                    self.audio_metadata[key],
                    self.audio_model.file.metadata[key])

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


class Mp3Test(AudioFieldMetadataTestCase):
    filename = 'test.mp3'
    filetype = 'mp3'
    playtime = '4'
    audio_metadata = {'album': u'from the internet',
                     'title': u'im chargin my laser',
                     'artist': u'armstrong',
                     'genre': u'Satire',
                     'date': u'2011',
                     'tracknumber': u'1'}


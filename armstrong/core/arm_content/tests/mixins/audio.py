# coding=utf-8
from django.db import models
from .._utils import *

from ..arm_content_support.models import AudioMixinModel

from ...fields import AudioField
from ..fields.audio import Mp3Test

AUDIO_FIELDS = {'file':AudioField,
                'playtime':models.PositiveIntegerField,
                'filetype':models.CharField, 
                'artist':models.CharField,
                'genre':models.CharField}

class AudioMixinTestCase(ArmContentTestCase):
    def test_models_mixed_in_with_AudioMixin_has_audio_fields(self):
        model = AudioMixinModel.objects.create()
        for (field, field_type) in AUDIO_FIELDS.items():
            self.assertModelHasField(model, field, field_type)

    def test_audio_model_works_when_cast_to_string(self):
        am = load_audio_model(filename = 'test.mp3', model = AudioMixinModel)        
        expected = "%s by %s on %s" % (am.file, am.artist, am.album)
        self.assertEqual(str(am), expected)

    def test_should_be_able_to_convert_to_unicode(self):
        am = load_audio_model(filename = 'test.mp3', model = AudioMixinModel)        
        expected = u"%s by %s on %s" % (am.file, am.artist, am.album)

        self.assertTrue(type(am.__unicode__()) is unicode)
        self.assertEqual(am.__unicode__(), expected)

    def test_html_player_output(self):
        am = load_audio_model(filename = 'test.mp3', model = AudioMixinModel)        
        self.assertEqual(am.html, am.file.render() )
